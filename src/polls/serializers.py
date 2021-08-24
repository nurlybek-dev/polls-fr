from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import datetime
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from .models import Poll, Question, Choice, Vote, Answer


class IDField(PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        try:
            value = self.get_queryset().get(pk=data)
            return value.id
        except ObjectDoesNotExist:
            self.fail('does_not_exist', pk_value=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'text')
        read_only_fields = ('id', )


class QuestionSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(
        choices=Question.Type.choices, default=Question.Type.TEXT
    )
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ('id','poll', 'text', 'type', 'choices')
        read_only_fields = ('id', )
    
    def create_choices(self, question, choices):
        Choice.objects.bulk_create([
            Choice(question=question, **data) for data in choices
        ])
    
    def create(self, validated_data):
        choices = validated_data.pop('choices', [])
        question = Question.objects.create(**validated_data)
        self.create_choices(question, choices)
        return question
    
    def update(self, instance, validated_data):
        choices = validated_data.pop('choices', [])
        instance.choices.all().delete()
        self.create_choices(instance, choices)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        
        instance.save()
        return instance


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Poll
        fields = ('id', 'title', 'start_date', 'end_date', 'description', 'questions')
        read_only_fields = ('id', )
    
    def validate_start_date(self, value):
        """
        Вернуть ошибку если меняется дата старта после создания опроса.
        """
        if self.instance and self.instance.start_date != value:
            raise serializers.ValidationError(
                "Дату старта нельзя менять"
            )
        
        return value
    

class AnswerSerializer(serializers.ModelSerializer):
    choice = ChoiceSerializer(read_only=True)
    choice_id = IDField(queryset=Choice.objects.all(), write_only=True)

    question = QuestionSerializer(read_only=True)
    question_id = IDField(queryset=Question.objects.all(), write_only=True)

    class Meta:
        model = Answer
        fields = ('id', 'question', 'question_id', 'choice', 'choice_id', 'value')
        read_only_fields = ('id', )


class VoteSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    poll = PollSerializer(read_only=True)
    poll_id = IDField(
        queryset=Poll.objects.filter(end_date__gte=datetime.today()),
        write_only=True
    )

    class Meta:
        model = Vote
        fields = ('id', 'poll_id', 'poll', 'user', 'date', 'answers')
        read_only_fields = ('id', 'date')

    def create(self, validated_data):
        answers = validated_data.pop('answers', [])
        instance = Vote.objects.create(**validated_data)
        Answer.objects.bulk_create([
            Answer(vote=instance, **data) for data in answers
        ])
        return instance
