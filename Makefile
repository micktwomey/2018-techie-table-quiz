.PHONY: all
all:
	pipenv run python generate_questions_and_answers.py
	cp *.jpg questions/
	cp *.jpg answers/
	cp *.png questions/
	cp *.png answers/

.PHONY: watch
watch:
	ls *.yml | entr make
