from dataclasses import dataclass
import collections
import pathlib
from pprint import pprint
import typing

import click
import yaml


@dataclass
class Question:
    question: str
    answer: str


@dataclass
class Round:
    title: str
    questions: typing.List[Question]

    @property
    def slug(self):
        return self.title.lower().replace(" ", "_")

@dataclass
class Quiz:
    rounds: typing.List[Round]


def parse_quiz(quiz):
    return Quiz(rounds=[parse_round(r) for r in quiz["rounds"]])


def parse_round(round):
    return Round(
        title=round["title"], questions=[parse_question(q) for q in round["questions"]]
    )


def parse_question(question):
    return Question(question=question["question"], answer=question["answer"])

ROUND_QUESTIONS_TEMPLATE = """theme: Huerta, 2

# {title}

---
{questions}

# End of Round!

## Pass Answer Sheets to the Next Team
"""

QUESTION_TEMPLATE = """
## Question {number}
{question}

---
"""

ANSWER_TEMPLATE = """
## Question {number}
{question}

{answer}

---
"""

ROUND_ANSWERS_TEMPLATE = """theme: Huerta, 2

# {title} Answers

---
{answers}

# End of Answers!

## Pass the Answer Sheets to the Quizmasters
"""

def render_questions(questions):
    output = []
    for i, question in enumerate(questions):
        output.append(QUESTION_TEMPLATE.format(number=i+1, question=question.question))
    return "\n".join(output)

def render_answers(questions):
    output = []
    for i, question in enumerate(questions):
        output.append(ANSWER_TEMPLATE.format(number=i+1, question=question.question, answer=question.answer))
    return "\n".join(output)


def render_quiz(quiz: Quiz, questions_folder: pathlib.Path, answers_folder: pathlib.Path):
    questions_folder.mkdir(parents=True, exist_ok=True)
    answers_folder.mkdir(parents=True, exist_ok=True)
    for round in quiz.rounds:
        questions = questions_folder / (round.slug + "_questions.md")

        with questions.open(mode="w") as fp:
            fp.write(ROUND_QUESTIONS_TEMPLATE.format(
                title=round.title,
                questions=render_questions(round.questions)
            ))

        answers = answers_folder / (round.slug + "_answers.md")

        with answers.open(mode="w") as fp:
            fp.write(ROUND_ANSWERS_TEMPLATE.format(
                title=round.title,
                answers=render_answers(round.questions)
            ))

@click.command()
@click.option(
    "--answers-folder", type=click.Path("answers", dir_okay=True), default="answers"
)
@click.option(
    "--questions-folder",
    type=click.Path("questions", dir_okay=True),
    default="questions",
)
@click.argument("questions", type=click.File(), default="all_questions.yml")
def main(answers_folder, questions_folder, questions):
    parsed = yaml.load(questions)
    quiz = parse_quiz(parsed)

    render_quiz(quiz, pathlib.Path(questions_folder), pathlib.Path(answers_folder))

if __name__ == "__main__":
    main()  # pylint: disable=E1120
