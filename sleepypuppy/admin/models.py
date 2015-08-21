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
from sqlalchemy import Column, Integer, ForeignKey
from sleepypuppy import db

# Database association models
user_associations = db.Table(
    'user_associations',
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('assessment_id', Integer, ForeignKey('assessments.id')),
)

assessment_associations = db.Table(
    'assessment_associations',
    Column('assessment_id', Integer, ForeignKey('assessments.id')),
    Column('payload', Integer, ForeignKey('payloads.id'))
)

taxonomy = db.Table(
    'taxonomy',
    Column('javascript_id', Integer, ForeignKey('javascript.id')),
    Column('payload', Integer, ForeignKey('payloads.id')),
)
