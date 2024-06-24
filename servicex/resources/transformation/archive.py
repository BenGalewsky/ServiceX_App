from servicex.decorators import auth_required
from servicex.models import TransformRequest, db
from servicex.resources.servicex_resource import ServiceXResource


class ArchiveTransform(ServiceXResource):

    @auth_required
    def get(self, request_id: str):
        transform_req = TransformRequest.lookup(request_id)
        if not transform_req:
            msg = f'Transformation request not found with id: {request_id}'
            self.logger.warning(msg)
            return {'message': msg}, 404
        elif transform_req.incomplete:
            msg = f"Transform request with id {request_id} is still in progress."
            self.logger.warning(msg)
            return {"message": msg}, 400

        # todo - Cleanup Minio here

        transform_req.archived = True
        transform_req.save_to_db()
        db.session.commit()

        return {"message": f"Archived transformation request {request_id}"}, 200
