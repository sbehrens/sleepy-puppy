import os
from flask.ext.restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError
from sleepypuppy import db, app
from sleepypuppy.admin.payload.models import Payload
from sleepypuppy.admin.capture.models import Capture
from sleepypuppy.admin.assessment.models import Assessment

# Request parser for API calls to Payload model
parser_payload = reqparse.RequestParser()
parser_payload.add_argument('assessments', type=list, required=False, location='json')
parser_payload.add_argument('payload', type=str, required=False, help="Payload Cannot Be Blank", location='json')
parser_payload.add_argument('url', type=str, location='json')
parser_payload.add_argument('method', type=str, location='json')
parser_payload.add_argument('parameter', type=str, location='json')
parser_payload.add_argument('notes', type=str, location='json')
# Request parser for API calls to Assessment model
parser_assessment = reqparse.RequestParser()
parser_assessment.add_argument('name', type=str, required=False, help="Assessment Name Cannot Be Blank", location='json')


class AssessmentView(Resource):
    """
    API Provides CRUD operations for Specific Assessment based on id.

    Methods:
    GET
    PUT
    DELETE

    """
    def get(self, id):
        """
        Retrieve an assessment based on id.
        """
        e = Assessment.query.filter(Assessment.id == id).first()
        if e is not None:
            return e.as_dict()
        else:
            return {}

    def put(self, id):
        """
        Update an assessment based on id.
        """
        args = parser_assessment.parse_args()
        e = Assessment.query.filter(Assessment.id == id).first()
        if e is not None:
            e.name = args["name"]
        try:
            db.session.commit()
        except IntegrityError, exc:
            return {"error": exc.message}, 500

        return e.as_dict(), 201

    def delete(self, id):
        """
        Delete an assessment based on id.
        """
        e = Assessment.query.filter(Assessment.id == id).first()
        if e is not None:
            try:
                db.session.delete(e)
                db.session.commit()
            except IntegrityError, exc:
                return {"error": exc.message}, 500
        else:
            return {}

        return e.as_dict(), 204


class AssessmentViewList(Resource):
    """
    API Provides CRUD operations for Assessments.

    Methods:
    GET
    POST
    """
    def get(self):
        results = []
        for row in Assessment.query.all():
            results.append(row.as_dict())
        return results

    def post(self):
        args = parser_assessment.parse_args()
        o = Assessment()
        o.name = args["name"]

        try:
            db.session.add(o)
            db.session.commit()
        except IntegrityError, exc:
            return {"error": exc.message}, 500

        return o.as_dict(), 201


class PayloadView(Resource):
    """
    API Provides CRUD operations for Payloads based on id.

    Methods:
    GET
    PUT
    DELETE
    """
    def get(self, id):
        e = Payload.query.filter(Payload.id == id).first()
        if e is not None:
            e.payload = e.payload.replace("$1", "//{}/c.js?u={}".format(app.config['HOSTNAME'], str(e.id)))
            return e.as_dict()
        else:
            return {}

    def put(self, id):
        args = parser_payload.parse_args()
        e = Payload.query.filter(Payload.id == id).first()
        if e is not None:
            for assessment_id in args["assessments"]:
                a = Assessment.query.filter(Assessment.id == assessment_id).first()
                if a is None:
                    return {"error": "Assessment not found!"}, 500
                e.assessments.append(a)

            e.payload = args["payload"].replace("$1", "//{}/c.js?u={}".format(app.config['HOSTNAME'], str(e.id)))
            e.url = args["url"]
            e.method = args["method"]
            e.parameter = args["parameter"]
            e.notes = args["notes"]

        try:
            db.session.commit()
        except IntegrityError, exc:
            return {"error": exc.message}, 500

        return e.as_dict(), 201

    def delete(self, id):
        e = Payload.query.filter(Payload.id == id).first()
        if e is not None:
            cascaded_captures = Capture.query.filter_by(payload_id=e.id).all()
            for capture in cascaded_captures:
                try:
                    os.remove("uploads/{}.png".format(capture.screenshot))
                    os.remove("uploads/small_{}.png".format(capture.screenshot))
                except:
                    pass
            try:
                db.session.delete(e)
                db.session.commit()
            except IntegrityError, exc:
                return {"error": exc.message}, 500
        else:
            return {}

        return e.as_dict(), 204


class PayloadViewList(Resource):
    """
    API Provides CRUD operations for Payloads.

    Methods:
    GET
    POST
    """
    def get(self):
        results = []
        for row in Payload.query.all():
            results.append(row.as_dict())
        return results

    def post(self):

        args = parser_payload.parse_args()
        o = Payload()
        o.payload = args["payload"].replace("$1", "//{}/c.js?u={}".format(app.config['HOSTNAME'], str(o.id)))
        o.url = args["url"]
        o.method = args["method"]
        o.parameter = args["parameter"]
        o.notes = args["notes"]

        for assessment_id in args["assessments"]:
            a = Assessment.query.filter(Assessment.id == assessment_id).first()
            if a is None:
                return {"error": "Assessment not found!"}, 500
            o.assessments.append(a)

        try:
            db.session.add(o)
            db.session.commit()
        except IntegrityError, exc:
            return {"error": exc.message}, 500

        return o.as_dict(), 201


class CaptureView(Resource):
    """
    API Provides CRUD operations for Captures based on id.

    Methods:
    GET
    DELETE

    Captures should be immutable so no PUT operations are permitted.
    """
    def get(self, id):
        e = Capture.query.filter(Capture.id == id).first()
        if e is not None:
            return e.as_dict()
        else:
            return {}

    def delete(self, id):
        capture = Capture.query.filter(Capture.id == id).first()
        if capture is not None:
            try:
                os.remove("uploads/{}.png".format(capture.screenshot))
                os.remove("uploads/small_{}.png".format(capture.screenshot))
            except:
                pass
            try:
                db.session.delete(capture)
                db.session.commit()
            except IntegrityError, exc:
                return {"error": exc.message}, 500
        else:
            return {}

        return capture.as_dict(), 204


class CaptureViewList(Resource):
    """
    API Provides CRUD operations for Captures.

    Methods:
    GET
    """
    def get(self):
        results = []
        for row in Capture.query.all():
            results.append(row.as_dict())
        return results

