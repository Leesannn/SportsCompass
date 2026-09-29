class Work24Router:
    """고용24 공고와 수집 상태를 PostgreSQL로 라우팅."""

    app_label = 'jobs'
    model_names = {'externaljobposting', 'work24fetchstatus'}
    database = 'community'

    def _is_target(self, model):
        return model._meta.app_label == self.app_label and model._meta.model_name in self.model_names

    def db_for_read(self, model, **hints):
        if self._is_target(model):
            return self.database
        return None

    def db_for_write(self, model, **hints):
        if self._is_target(model):
            return self.database
        return None

    def allow_relation(self, obj1, obj2, **hints):
        is1, is2 = self._is_target(type(obj1)), self._is_target(type(obj2))
        if is1 or is2:
            return is1 and is2
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == self.app_label and model_name in self.model_names:
            return db == self.database
        if db == self.database and app_label == self.app_label:
            # jobs 앱에서 고용24 수집 모델 외의 테이블은 PostgreSQL에 만들지 않는다.
            return False
        return None


class CommunityRouter:
    """Route all community app database operations to PostgreSQL."""

    app_label = 'community'
    database = 'community'

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return self.database
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return self.database
        return None

    def allow_relation(self, obj1, obj2, **hints):
        app1 = obj1._meta.app_label
        app2 = obj2._meta.app_label

        if self.app_label in {app1, app2}:
            return app1 == app2
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == self.app_label:
            return db == self.database
        if db == self.database:
            return False
        return None
