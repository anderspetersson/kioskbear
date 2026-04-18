from ninja import NinjaAPI, Schema

from ..feedback.models import Rating
from .models import Block, Survey

api = NinjaAPI(version="1.0.0")


class RatingSchema(Schema):
    score: int
    survey: int


def render_block_detail(block: Block):
    return {
        "id": block.id,
        "title": block.title,
        "options": render_option_list(block),
        "scored_options": render_scored_option_list(block),
    }


def render_option_detail(option):
    if option.follow_up_block:
        return {
            "id": option.id,
            "text": option.text,
            "follow_up_block": render_block_detail(option.follow_up_block),
        }
    else:
        return {
            "id": option.id,
            "text": option.text,
        }


def render_scored_option_detail(scored_option):
    if scored_option.follow_up_block:
        return {
            "id": scored_option.id,
            "text": scored_option.text,
            "score": scored_option.score,
            "follow_up_block": render_block_detail(scored_option.follow_up_block),
        }
    else:
        return {
            "id": scored_option.id,
            "text": scored_option.text,
            "score": scored_option.score,
        }


def render_option_list(block: Block):
    return [render_option_detail(option) for option in block.options.all()]


def render_scored_option_list(block: Block):
    return [
        render_scored_option_detail(scored_option)
        for scored_option in block.scored_options.all()
    ]


@api.get("/survey")
def survey(request, id: int):
    survey_object = Survey.objects.get(pk=id)
    block_list = Block.objects.filter(survey=survey_object).select_related()

    return {
        "id": survey_object.id,
        "start_block": render_block_detail(survey_object.start_block),
        "end_block": render_block_detail(survey_object.end_block),
        "block_list": [render_block_detail(block) for block in block_list],
    }


@api.post("/ratings/")
def ratings(request, rating: RatingSchema):
    rating = Rating.objects.create(
        score=rating.dict().get("score"),
        survey=Survey.objects.get(pk=rating.dict().get("survey")),
    )
    return {"id": rating.id}
