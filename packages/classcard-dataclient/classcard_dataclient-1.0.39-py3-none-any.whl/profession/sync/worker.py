from sync.student import StudentSync
from sync.teacher import TeacherSync
from sync.clas import ClassSync
from sync.classroom import ClassroomSync
from sync.course import CourseSyncV1
from sync.subject import SubjectSync
from sync.school import SchoolSync


def start_sync_v1():
    school_sync = SchoolSync()
    school_sync.start()
    index, total = 0, len(school_sync.school_map)
    for name, number in school_sync.school_map.items():
        index += 1
        print(">>> Start Sync {} Data, Process {}/{}".format(name, index, total))
        school_info = {"school_name": name, "school_number": number}
        teacher_sync = TeacherSync(**school_info)
        teacher_sync.start()
        class_sync = ClassSync(**school_info)
        class_sync.start()
        student_sync = StudentSync(class_entrance=class_sync.class_entrance, **school_info)
        student_sync.start()
        classroom_sync = ClassroomSync(**school_info)
        classroom_sync.start()
        subject_sync = SubjectSync(**school_info)
        subject_sync.start()
        course_sync = CourseSyncV1(**school_info)
        course_sync.start()


start_sync_v1()
