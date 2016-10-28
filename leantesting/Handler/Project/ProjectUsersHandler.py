from BaseClass.EntityList       import EntityList
from BaseClass.EntityHandler    import EntityHandler
from BaseClass.APIRequest       import APIRequest

from Entity.Project.ProjectUser import ProjectUser

class ProjectUsersHandler(EntityHandler):

	_projectID = None

	def __init__(self, origin, projectID):
		super().__init__(origin)

		self._projectID = projectID

	def all(self, filters = None):
		if filters is None:
			filters = {}

		super().all(filters)

		request = APIRequest(self._origin, '/v1/projects/' + str(self._projectID) + '/users', 'GET')
		return EntityList(self._origin, request, ProjectUser, filters)
