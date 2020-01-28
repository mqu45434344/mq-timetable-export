
import io

class TimetableExporter:
    def dump(self, study_period, file):
        raise NotImplementedError

    def dumps(self, study_period):
        output = io.StringIO()
        self.dump(study_period, output)
        return output.getvalue()
