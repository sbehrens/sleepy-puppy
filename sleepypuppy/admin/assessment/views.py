#     Copyright 2015 Netflix, Inc.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
from flask.ext.admin.contrib.sqla import ModelView
from models import Assessment
from sleepypuppy.admin.payload.models import Payload
from flask.ext import login
from flask_wtf import Form
from sleepypuppy import app
import collections


@app.context_processor
def utility_processor():
    def get_payloads():
        the_payloads = Payload.query.all()
        results = collections.OrderedDict()
        for i in the_payloads:
            results[i] = i.payload
        return results
    return dict(get_payloads=get_payloads)



class AssessmentView(ModelView):
    """
    ModelView override of Flask Admin for Assessments.
    """
    # CSRF Protecdtion
    form_base_class = Form

    # Check if user is authenticated
    def is_accessible(self):
        return login.current_user.is_authenticated()

    list_template = 'assessment_list.html'

    # Only display form columns listed below
    form_columns = ['name', 'access_log_enabled']

    column_list = ['name', 'payloads']
    form_args = dict(
        access_log_enabled=dict(
            description="Record requests to payloads regardless if \
            they executed to the 'Access Log' \
            table for any payload associated with this assessment. \
            Recommended if you think you may hit namespace\
            conflicts or issues running JS payloads in victim's browser"
        )
    )

    column_formatters = dict(
        payloads=lambda v, c, m, p: [Payload.query.all()])


    def __init__(self, session, **kwargs):
        super(AssessmentView, self).__init__(Assessment, session, **kwargs)
