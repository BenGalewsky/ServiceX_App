# Copyright (c) 2019, IRIS-HEP
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import logging
import datetime

from flask_restful import reqparse
from servicex.models import db
from servicex.resources.servicex_resource import ServiceXResource
from servicex.models import FileStatus, max_string_size


class FileTransformationStatus(ServiceXResource):

    def __init__(self):
        self.status_parser = reqparse.RequestParser()
        self.status_parser.add_argument('timestamp', help='This field cannot be blank',
                                        required=True)
        self.status_parser.add_argument('status-code', help='This field cannot be blank',
                                        required=True)
        self.status_parser.add_argument('pod-name', required=False)
        self.status_parser.add_argument('info', required=False)

        logger = logging.getLogger(__name__)
        logger.addHandler(logging.NullHandler())
        self.logger = logger

    def post(self, request_id, file_id):
        status = self.status_parser.parse_args()
        print(status)
        status.request_id = request_id
        file_status = FileStatus(file_id=file_id, request_id=request_id,
                                 timestamp=datetime.datetime.strptime(
                                     status.timestamp,
                                     "%Y-%m-%dT%H:%M:%S.%f"),
                                 pod_name=status['pod-name'],
                                 status=status['status-code'],
                                 info=status.info[:max_string_size])
        file_status.save_to_db()
        self.logger.info(f"Saved file status: {file_status}")
        try:
            db.session.commit()
        except Exception:
            self.logger.exception("Error saving file status record")
        finally:
            return "Ok"
