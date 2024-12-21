from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse, FileResponse
from django.urls import reverse
from .models import datosUsuario, publicacion, comentario
import json
import base64
from django.contrib.auth.models import User


def ingresoUsuario(request):
    if request.method == 'POST':
        nombreUsuario = request.POST.get('nombreUsuario')
        contraUsuario = request.POST.get('contraUsuario')
        usrObj = authenticate(request,username=nombreUsuario, password=contraUsuario)
        if usrObj is not None:
            login(request,usrObj)
            return HttpResponseRedirect(reverse('app3:informacionUsuario'))
        else:
            return HttpResponseRedirect(reverse('app3:ingresoUsuario'))
    return render(request,'ingresoUsuario.html')

@login_required(login_url='/')
def informacionUsuario(request):
    return render(request,'informacionUsuario.html',{
        'allPubs':publicacion.objects.all()
    })


@login_required(login_url='/')
def cerrarSesion(request):
    logout(request)
    return render(request,'ingresoUsuario.html')

def ejemploJs(request):
    return render(request,'ejemploJs.html')

def devolverDatos(request):
    return JsonResponse(
        {
            'nombreCurso':'DesarroloWebPython',
            'horario':{
                'martes':'7-10',
                'jueves':'7-10'
            },
            'backend':'django',
            'frontend':'reactjs',
            'cantHoras':24
        }
    )

def devolverAllPubs(request):
    objPub = publicacion.objects.all()
    listaPublicacion = []
    for obj in objPub:
        listaPublicacion.append(
            {
                'titulo':obj.titulo,
                'descripcion':obj.descripcion
            }
        )
    return JsonResponse({
        'listaPublicacion':listaPublicacion
    })

def devolverPublicacion(request):
    idPub = request.GET.get('idPub')
    try:
        datosComentarios = []
        objPub = publicacion.objects.get(id=idPub)
        comentariosPub = objPub.comentario_set.all()
        for comentarioInfo in comentariosPub:
            datosComentarios.append({
                'autor': f"{comentarioInfo.autoCom.first_name} {comentarioInfo.autoCom.last_name}",
                'descripcion': comentarioInfo.descripcion
            })
        try:
            with open(objPub.imagenPub.path,'rb') as imgFile:
                imgPub = base64.b64encode(imgFile.read()).decode('UTF-8')
        except:
            imgPub = None

        return JsonResponse({
            'titulo': objPub.titulo,
            'autor':f"{objPub.autorPub.first_name} {objPub.autorPub.last_name}",
            'descripcion':objPub.descripcion,
            'datosComentarios': datosComentarios,
            'imgPub':imgPub
        })
    except:
        return JsonResponse({
            'titulo':'SIN DATOS',
            'autor':'SIN DATOS',
            'descripcion':'SIN DATOS',
            'datosComentarios':None,
            'imgPub':None
        })
    
def publicarComentario(request):
    datosComentario = json.load(request)
    print(datosComentario)
    comentarioTexto = datosComentario.get('comentario')
    idPublicacion = datosComentario.get('idPublicacion')
    objPublicacion = publicacion.objects.get(id=idPublicacion)
    comentario.objects.create(
        descripcion = comentarioTexto,
        pubRel = objPublicacion,
        autoCom = request.user
    )
    return JsonResponse({
        'resp':'ok'
    })

def crearPublicacion(request):
    if request.method == 'POST':
        tituloPub = request.POST.get('tituloPub')
        descripcionPub = request.POST.get('descripcionPub')
        autorPub = request.user
        imagenPub = request.FILES.get('imagenPub')

        publicacion.objects.create(
            titulo=tituloPub,
            descripcion=descripcionPub,
            autorPub = autorPub,
            imagenPub = imagenPub
        )

        return HttpResponseRedirect(reverse('app3:informacionUsuario'))
    
def inicioReact(request):
    return render(request, 'inicioReact.html')

"""
PREGUNTA 1 - B
CREAR EL IF QUE PERMITA RECONOCER EL MÉTODO DE LA PETICION:
IF REQUEST.METHOD == ....
DENTRO DE LA SELECTIVA CAPTURAR LOS DATOS DEL FORMULARIO : 
USERNAMEUSUARIO = REQUEST.POST.GET('USE ...
...

CREAR EL OBJETO USER CON USERNAME E EMAIL : 

OBJUSR = USER.OBJECTS.CREATE(
    USERNAME = ... ,
    EMAIL = ... 
)

LUEGO SETEAR LA CONTRASEÑA CON LA FUNCION SET_PASSWORD:
CONTRAUSUARIO = REQUEST.POST.GET('CONTRAUSUARIO')
OBJUSR.SET_PASSWORD(CONTRAUSUARIO) ...

FINALMENTE CREAR EL REGISTRO EN DATOSUSUARIO Y RELACIONARLO CON EL
OBJETO OBJUSR - RECORDAR LA RELACION ONE TO ONE Y COMO SE CREO
EL USUARIO EN LA CLASES 5 Y 6

FINALMENTE REDIRECCIONAR A LA MISMA RUTA DE CONSOLAADMINISTRADOR - return HttpResponseRedirect(reverse('app3:consolaAdministrador'))

EJEMPLO DE CREACION DE NUEVO USUARIO:

usernameUsuario = request.POST.get('usernameUsuario')
contraUsuario = request.POST.get('contraUsuario')
nombreUsuario = request.POST.get('nombreUsuario')
apellidoUsuario = request.POST.get('apellidoUsuario')
emailUsuario = request.POST.get('emailUsuario')
profesionUsuario = request.POST.get('profesionUsuario')
nroCelular = request.POST.get('nroCelular')
perfilUsuario = request.POST.get('perfilUsuario')

nuevoUsuario = User.objects.create(
    username=usernameUsuario,
    email=emailUsuario
)
nuevoUsuario.set_password(contraUsuario)
nuevoUsuario.first_name = nombreUsuario
nuevoUsuario.last_name = apellidoUsuario
nuevoUsuario.is_staff = True
nuevoUsuario.save()


datosUsuario.objects.create(
    profesion=profesionUsuario,
    nroCelular=nroCelular,
    perfilUsuario=perfilUsuario,
    usrRel=nuevoUsuario
)

"""

def crearUsuario(request):
    if request.method == 'POST':
        usernameUsuario = request.POST.get('usernameUsuario')
        contraUsuario = request.POST.get('contraUsuario')
        nombreUsuario = request.POST.get('nombreUsuario')
        apellidoUsuario = request.POST.get('apellidoUsuario')
        emailUsuario = request.POST.get('emailUsuario')
        profesionUsuario = request.POST.get('profesionUsuario')
        nroCelular = request.POST.get('nroCelular')
        perfilUsuario = request.POST.get('perfilUsuario')

        nuevoUsuario = User.objects.create(
            username=usernameUsuario,
            email=emailUsuario
        )

        nuevoUsuario.set_password(contraUsuario)
        nuevoUsuario.first_name = nombreUsuario
        nuevoUsuario.last_name = apellidoUsuario
        nuevoUsuario.is_staff = True
        nuevoUsuario.save()

        datosUsuario.objects.create(
            profesion=profesionUsuario,
            nroCelular=nroCelular,
            perfilUsuario=perfilUsuario,
            usrRel=nuevoUsuario    
        )

        return HttpResponseRedirect(reverse('app3:consolaAdministrador'))

@login_required(login_url='/')
def consolaAdministrador(request):
    allUsers = User.objects.all().order_by('id')
    return render(request,'consolaAdministrador.html',{
        'allUsers':allUsers
    })


"""
    Pregunta 3
    Esta funcion devolvera los campos que se necesitan 
    cargar en la ventana modal para poder ser editados
    Con el id del usuario se puede obtener el objeto y devolver
    el objeto Json con la informacion necesaria.
"""

def obtenerDatosUsuario(request):
    idUsuario = request.GET.get('idUsuario')
    try:
        objUser = User.objects.get(id=idUsuario)
    
        return JsonResponse({
                'usernameUsuario': objUser.username,
                'nombreUsuario': objUser.first_name,
                'apellidoUsuario': objUser.last_name,
                'emailUsuario': objUser.email,
                'profesionUsuario': objUser.datosusuario.profesion,
                'nroCelular':objUser.datosusuario.nroCelular,
                'perfilUsuario':objUser.datosusuario.perfilUsuario                
        })
    except:
        return JsonResponse({
            'usernameUsuario': objUser.username,
            'nombreUsuario': objUser.first_name,
            'apellidoUsuario': objUser.last_name,
            'emailUsuario': objUser.email,
            'profesionUsuario':'Sin datos',
            'usernameUsuario': 'Sin datos',
            'nombreUsuario': 'Sin datos',
            'nroCelular':'Sin datos',
            'perfilUsuario':'Sin datos'
    })

def actualizarUsuario(request):
    """
    Pregunta 5
    En esta funcion recibira los datos del formulario de actualizacion de usuario
    Debe capturar dichos datos, recuerde que en el input con atributo name idUsuario
    se ha cargado el id del usuario correspondiente lo que le permitira obtener el objeto
    de la base de datos. Con el objeto capturado modificar los campos respectivos y finalmente
    ejecutar el metodo save() para su respectiva actualizacion
    """
    if request.method == 'POST':
        idUsuario = request.POST.get('idUsuario')
        nombreUsuario = request.POST.get('nombreUsuario')
        apellidoUsuario = request.POST.get('apellidoUsuario')
        profesionUsuario = request.POST.get('profesionUsuario')
        nroCelular = request.POST.get('nroCelular')
        perfilUsuario = request.POST.get('perfilUsuario')          

        usuario_act = User.objects.get(id=idUsuario)
        usuario_act.first_name = nombreUsuario
        usuario_act.last_name = apellidoUsuario
        usuario_act.datosusuario.perfilUsuario = perfilUsuario
        usuario_act.datosusuario.profesion = profesionUsuario
        usuario_act.datosusuario.nroCelular = nroCelular
        usuario_act .save()    

    return HttpResponseRedirect(reverse('app3:consolaAdministrador'))

