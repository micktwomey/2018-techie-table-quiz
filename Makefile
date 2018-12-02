.PHONY: all
all:
	pipenv run python generate_questions_and_answers.py

.PHONY: watch
watch:
	ls *.yml | entr make
