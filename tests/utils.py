from study.models import Course, PassAccess, Lesson


def create_lesson(course):
    lessons_count = 0
    lessons_data = [
        {
            'course': course,
            'name': 'TestLesson01',
            'link_to_video': 'https://www.youtube.com/watch?v=hqYUAVobDJA',
        },
        {
            'course': course,
            'name': 'TestLesson02',
            'link_to_video': 'https://www.youtube.com/watch?v=l36FuBLNZCA',
        },
        {
            'course': course,
            'name': 'TestLesson03',
            'link_to_video': 'https://www.youtube.com/watch?v=10Uw0AyGFvU',
        },
    ]
    for data in lessons_data:
        Lesson.objects.create(**data)
        lessons_count += 1
    return lessons_count


def create_users_data(need_users=3):
    return [
        {'username': f'TestUser{n}', 'password': 'test_password22'}
        for n in range(1, need_users + 1)
    ]


def create_pa(user_data, user_model, course):
    users_count = 0
    for data in user_data:
        user = user_model.objects.create(**data)
        PassAccess.objects.create(student=user, course=course, is_valid=True)
        users_count += 1
    return users_count
