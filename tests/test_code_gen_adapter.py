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
import pytest

from servicex.code_gen_adapter import CodeGenAdapter


class TestCodeGenAdapter:
    def test_init(self, mocker):
        service = CodeGenAdapter("http://foo.com")
        assert service.code_gen_url == "http://foo.com"

    def test_generate_code_for_selection(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_requests_post = mocker.patch('requests.post', return_value=mock_response)
        service = CodeGenAdapter("http://foo.com")
        service.generate_code_for_selection("test-tring")
        mock_requests_post.assert_called()

    def test_generate_code_bad_response(self, mocker):
        mock_response = mocker.Mock()
        mock_response.status_code = 500
        mock_response.json = {"Message": "Ooops"}
        mocker.patch('requests.post', return_value=mock_response)
        service = CodeGenAdapter("http://foo.com")

        with pytest.raises(BaseException) as eek:
            service.generate_code_for_selection("test-tring")
        assert str(eek.value) == 'Failed to generate translation code: Ooops'
