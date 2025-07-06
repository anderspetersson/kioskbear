from django import template
from django.template import loader
from kioskbear.kiosk.models import Block
from kioskbear.feedback.models import Option, ScoredOption, FormField


register = template.Library()


@register.simple_tag(takes_context=True)
def render_block(context, id: int):
    block = Block.objects.get(pk=id)
    if Option.objects.filter(block=block):
        template_name = 'app/template_tags/block_question.html'
    elif ScoredOption.objects.filter(block=block):
        template_name = 'app/template_tags/block_rate.html'
    elif FormField.objects.filter(block=block):
        template_name = 'app/template_tags/block_form.html'
    elif block.pk == block.survey.end_block.pk:
        template_name = 'app/template_tags/end_block.html'
    else:
        template_name = 'app/template_tags/block_empty.html'
    t = loader.get_template(template_name)
    context = context.flatten()
    context['block'] = block
    if block.pk == block.survey.end_block.pk or block.pk == block.survey.start_block.pk:
        context['allow_delete_block'] = False
    else:
        context['allow_delete_block'] = True
    return t.render(context)


@register.simple_tag(takes_context=True)
def render_block_title(context, block: Block):
    template_name = 'app/template_tags/block_title.html'
    t = loader.get_template(template_name)
    context = context.flatten()
    context['block'] = block
    return t.render(context)


@register.simple_tag(takes_context=True)
def render_block_options(context, block: Block):
    template_name = 'app/template_tags/block_button_options.html'
    t = loader.get_template(template_name)
    context = context.flatten()
    context['block'] = block
    return t.render(context)


@register.simple_tag(takes_context=True)
def render_block_scored_options(context, block: Block):
    template_name = 'app/template_tags/block_scored_options.html'
    t = loader.get_template(template_name)
    context = context.flatten()
    context['block'] = block
    return t.render(context)


def remove_option_parent_from_open_questions(question_lists, optionid):
    """
    Taken a list of open questions, remove the id from the list if its in the questions options follow_up.
    """

    question_to_look_for_option_follow_ups = Option.objects.get(pk=optionid).block
    question_lists = question_lists.split(',')
    for o in question_to_look_for_option_follow_ups.options.all():
        if o.follow_up_block:
            if str(o.follow_up_block.pk) in question_lists:
                question_lists.remove(str(o.follow_up_block.pk))
    question_lists = ','.join(question_lists)
    return question_lists


def get_question_object_from_option_id(optionid):
    return Option.objects.get(pk=optionid).block


register.filter("remove_option_parent_from_open_questions", remove_option_parent_from_open_questions)
register.filter("get_question_object_from_option_id", get_question_object_from_option_id)
