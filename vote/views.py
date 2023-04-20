from django.shortcuts import render
from . forms import VoterRegistrationForm
from . models import *


# Create your views here.
def index(request):

    voter_registration_form = VoterRegistrationForm()

    if request.method == 'POST':
        voter_registration_form = VoterRegistrationForm(request.POST)

        if voter_registration_form.is_valid():
            voter_info = voter_registration_form.cleaned_data

            zip_code = ZipCode.objects.filter(zip=voter_info['zip_code']).first()

            if zip_code:
                # Check if voter exists and if not add them to the database
                voter = Voter.objects.filter(first_name=voter_info['first_name'], last_name=voter_info['last_name'], age_range=voter_info['age_range'], zip_code=zip_code).first()
                if voter is None:
                    voter = Voter(first_name=voter_info['first_name'], last_name=voter_info['last_name'], age_range=voter_info['age_range'], zip_code=zip_code)
                    voter.save()

                # Extract questions from the form post
                questions = dict()
                for key in request.POST:
                    if key != "first_name" and key != "last_name" and key != "age_range" and key != "zip_code" and key != "csrfmiddlewaretoken":
                        # Check if each question_id is valid
                        question = Question.objects.filter(question_id=key).first()
                        value = request.POST[key]
                        if question:
                            if value == "yes":
                                value = True

                            if value == "no":
                                value = False

                            questions[question] = value

                # Check if voter has already voted on this question
                for question in questions:
                    voter_question = VoterQuestion.objects.filter(voter=voter, question=question).first()
                    if voter_question is None:
                        # Add the voter to the VoterQuestion table
                        voter_question = VoterQuestion(voter=voter, question=question)
                        voter_question.save()

                        # Add the vote to the Vote table
                        vote = Vote(question=question, vote=questions[question], vote_zip=voter.zip_code.zip, vote_age=voter.age_range)
                        vote.save()

                # Redirect to the results page
                return render(request, 'vote/thankyou.html')

    questions = Question.objects.all()

    context = {
        'form': voter_registration_form,
        'questions': questions,
    }

    return render(request, 'vote/index.html', context=context)


def results(request):

    # Tally the votes for each question
    questions = Question.objects.all()
    for question in questions:
        yes_votes = Vote.objects.filter(question=question, vote=True).count()
        no_votes = Vote.objects.filter(question=question, vote=False).count()
        question.total_votes = yes_votes + no_votes
        question.yes_votes = yes_votes
        question.no_votes = no_votes

    context = {
        'questions': questions,
    }

    return render(request, 'vote/results.html', context=context)


def question_results(request, question_id):
    question = Question.objects.filter(question_id=question_id).first()
    yes_votes = Vote.objects.filter(question=question, vote=True).count()
    no_votes = Vote.objects.filter(question=question, vote=False).count()
    question.total_votes = yes_votes + no_votes
    question.yes_votes = yes_votes
    question.no_votes = no_votes

    # Group votes by age range
    age_ranges = AgeRange.objects.all()
    for age_range in age_ranges:
        yes_votes = Vote.objects.filter(question=question, vote=True, vote_age=age_range).count()
        no_votes = Vote.objects.filter(question=question, vote=False, vote_age=age_range).count()
        age_range.total_votes = yes_votes + no_votes
        age_range.yes_votes = yes_votes
        age_range.no_votes = no_votes

    # Get all zip codes from votes
    zip_codes = Vote.objects.filter(question=question).values('vote_zip').distinct()

    for zip_code in zip_codes:

        zc = ZipCode.objects.filter(zip=zip_code['vote_zip']).first()

        yes_votes = Vote.objects.filter(question=question, vote=True, vote_zip=zc).count()
        no_votes = Vote.objects.filter(question=question, vote=False, vote_zip=zc).count()

        zip_code['yes_votes'] = yes_votes
        zip_code['no_votes'] = no_votes

    '''
    # Group votes by zip code
    zip_codes = ZipCode.objects.all()
    for zip_code in zip_codes:
        yes_votes = Vote.objects.filter(question=question, vote=True, vote_zip=zip_code).count()
        no_votes = Vote.objects.filter(question=question, vote=False, vote_zip=zip_code).count()
        zip_code.total_votes = yes_votes + no_votes
        zip_code.yes_votes = yes_votes
        zip_code.no_votes = no_votes
    '''

    context = {
        'question': question,
        'age_ranges': age_ranges,
        'zip_codes': zip_codes,
    }

    return render(request, 'vote/question_results.html', context=context)