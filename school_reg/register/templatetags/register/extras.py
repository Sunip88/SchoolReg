#!/usr/bin/python3.7
from django import template


register = template.Library()


# @register.filter()
# def count_comments(photo):
#     comments = Comments.objects.filter(photo_id=photo.id)
#     return len(comments)

