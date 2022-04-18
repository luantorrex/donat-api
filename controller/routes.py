from controller.auth.auth import Login, Logout, Register
from controller.institution import InstituicaoById, Institution, RetrieveInstitutionImage, RetrieveRandomInstitutions
from controller.user import getLoggedUser, profileImage
from services.institution_request import deleteInstitutionRequestById, requestInstitutionHandler, requestInstitutionImage


def initialize_routes(api):    
    api.add_resource(Institution, "/api/instituicao")
    api.add_resource(InstituicaoById, "/api/instituicao/<string:id>")
    api.add_resource(RetrieveInstitutionImage, "/api/instituicao/get_image/<string:id>")
    api.add_resource(RetrieveRandomInstitutions, "/api/instituicao/random")
    
    api.add_resource(requestInstitutionHandler, "/api/institution_request")
    api.add_resource(deleteInstitutionRequestById, "/api/institution_request/<string:id>")
    api.add_resource(requestInstitutionImage, "/api/institution_request/reqinstitution_image/<string:id>")
    
    api.add_resource(Login, "/api/login")
    api.add_resource(Register, "/api/register")
    api.add_resource(Logout, "/api/logout")
    
    api.add_resource(getLoggedUser, "/api/get_logged_user")
    api.add_resource(profileImage, "/api/profile_image")