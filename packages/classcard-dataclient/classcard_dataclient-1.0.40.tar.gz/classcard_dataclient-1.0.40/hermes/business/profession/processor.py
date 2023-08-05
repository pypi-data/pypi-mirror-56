from business.profession.action import upload_student_attendance


class ProfessionProcessor(object):
    KIND_FUNC = {"OpenStudentAttendance": "upload_student_attendance"}

    @classmethod
    def distribute(cls, topic, payload):
        try:
            data = payload['data']
            kind, content = data["kind"], data["extra"]
        except (Exception,):
            return
        try:
            if kind in cls.KIND_FUNC:
                getattr(cls, cls.KIND_FUNC[kind])(content)
        except (Exception,):
            import traceback
            print(traceback.print_exc())

    @staticmethod
    def upload_student_attendance(content):
        upload_student_attendance(content)
