from services.auth.auth import Login, Logout, Register, protected
from services.boleto import boleto
from services.institution import InstituicaoById, Institution, RetrieveInstitutionImage, RetrieveRandomInstitutions
from services.auth.reset_password import ForgotPassword, ResetPassword
from services.user import getLoggedUser, profileImage
from services.institution_request import deleteInstitutionRequestById, requestInstitutionHandler, requestInstitutionImage


def initialize_routes(api):
    #Instiution endpoints
    api.add_resource(Institution, "/api/instituicao")
    api.add_resource(InstituicaoById, "/api/instituicao/<string:id>")
    api.add_resource(RetrieveInstitutionImage, "/api/instituicao/get_image/<string:id>")
    api.add_resource(RetrieveRandomInstitutions, "/api/instituicao/random")
    
    
    #Instiution request endpoints 
    api.add_resource(requestInstitutionHandler, "/api/institution_request")
    api.add_resource(deleteInstitutionRequestById, "/api/institution_request/<string:id>")
    api.add_resource(requestInstitutionImage, "/api/institution_request/reqinstitution_image/<string:id>")
    
    #auth endpoints
    api.add_resource(Login, "/api/login")
    api.add_resource(Register, "/api/register")
    api.add_resource(Logout, "/api/logout")
    api.add_resource(ForgotPassword, '/api/forgot')
    api.add_resource(ResetPassword, '/api/reset')
    api.add_resource(protected, "/api/protected")
    
    
    api.add_resource(getLoggedUser, "/api/get_logged_user")
    api.add_resource(profileImage, "/api/profile_image")
    
    api.add_resource(boleto, "/api/get_boleto")