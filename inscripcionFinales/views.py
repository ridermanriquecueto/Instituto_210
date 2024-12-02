
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView    
from .models import *
from .forms import *
from django.views.generic import CreateView,TemplateView,ListView,UpdateView,DeleteView
from django.core.mail import send_mail
from django.contrib.auth import *
from django.contrib import messages
from django.db.models import Q,Prefetch,OuterRef,F
from django import forms
from datetime import datetime   
from django.http import HttpResponse,JsonResponse
import csv
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.core.paginator import *
from django.db import IntegrityError,models
from django.utils import timezone
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.decorators.csrf import csrf_protect
from math import *
from json import *
from django.template import loader
#from weasyprint import HTML, CSS

# Create your views here.

class ArchivoForm(forms.Form):
    archivo_csv = forms.FileField(label = 'Seleccione un archivo csv', required=False)

class HomePageView(TemplateView):
    template_name = 'index.html'
    model=Usuario

    def get(self, request):
        return  render(request, 'index.html')
    

class CustomLoginView(LoginView):
  pass

       
class CustomLogoutView(LogoutView):

    def get(self,request):
        logout(request)
        messages.success(request, 'Su sesión se ha cerrado correctamente. Hasta la próxima!')
        return redirect("/")



class registerView(CreateView):
    
    model = Usuario
    form_class = registri_user_form
    

    def form_valid(self, form):
        
        usuario = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        password = form.cleaned_data.get('password2')
        usuario = authenticate(email=email, password=password)
    
        
        form.save()
        #login(self.request, usuario)
        
        #send_mail('subject', f'\n-Su Usuario es: {email} \n- Su contraseña es: {password}\nLink para cambiar contraseña es: http://http://127.0.0.1:8000/change_password/<int:pk>,',from_email='webmaster.isfdyt210@gmail.com',recipient_list = [email])
        
        return redirect('/user_list')
    

   
       
class editUser(UpdateView):
    model = Usuario
    form_class = profile_students_form
    template_name = 'registration/edit_profile.html'
    success_url = '/'
    
class editMesa(UpdateView):
    model = MesaFinal
    form_class = MesaFinalForm
    template_name = 'registration/edit_mesa.html'
    success_url = '/mesas_lista/'
    
class editInscr(UpdateView):
    model = InscripcionFinal
    form_class = InscripcionFinalForm
    template_name = 'registration/edit_inscr.html'
    success_url = '/'

class cargarNotaFinal(UpdateView):
    model = InscripcionFinal
    form_class = InscripcionFinalForm
    template_name = 'finales/cargar_nota.html'
    success_url = '/'   
     
class profileviews(TemplateView):
    model = Usuario 
  

class deleteUser(DeleteView):
    model = Usuario
    template_name ='registration/delete_user.html'
    success_url = '/user_list'
    
class deleteInscripcion(DeleteView):
    model = InscripcionFinal
    template_name ='registration/delete_inscripcion.html'
    success_url = '/inscripcion_finales_lista'

class deleteMesa(DeleteView):
    model = MesaFinal
    template_name ='registration/delete_mesa.html'
    success_url = '/mesas_lista'
         

class institutoView(CreateView):
    model = Instituto
    form_class = institutoForms

    def form_valid(self, form):
        form.save()
        Instituto = form.cleaned_data.get('nombre_instituto')
        email = form.cleaned_data.get('email_instituto')
      
        
        return redirect('/')
    

class carreraView(CreateView):
       
    model = Carrera
    form_class = carreraForm

    def form_valid(self, form):
        form.save()
        Carrera = form.cleaned_data.get('nombre_carrera')
        Resolucion = form.cleaned_data.get('num_resolucion')
      
        
        return redirect('/')

class listUser(ListView):
    model = Usuario
    usuario=Usuario.objects.all()
    template_name = 'registration/list_user.html'
    
class listInscripcion(ListView):
    model = InscripcionFinal
    template_name = 'registration/list_inscripcion.html'

class listMesa(ListView):
    model = MesaFinal
    template_name = 'registration/mesas_finales_lista.html'
   
   
class showUser(ListView):
    model = Usuario
    template_name = 'registration/show_user.html'


def lista_materias_user(request):
    usuario = request.user.id
    materias_disponibles = []
    materias = Materia.objects.all()
    for materia in materias:
        if validar_inscripcion_materias(usuario, materia.id) and materia.inscripcionAbierta:
            materias_disponibles.append(materia)
    return render(request, 'materias/lista_materias_disponibles_user.html', {'materias': materias_disponibles})

def lista_materias_inscriptas_user(request):
    usuario = request.user.id
    materias_inscriptas = usuarios_materia.objects.filter(
        usuario_id=usuario,
        aprobada=False
    ).select_related('materia')
    
    return render(request, 'materias/lista_materias_inscriptas_user.html', {'materias': materias_inscriptas})

def lista_materias_inscriptas_adm(request):
    materias_inscriptas = usuarios_materia.objects.select_related('materia')
    return render(request, 'materias/lista_materias_inscriptas_adm.html', {'materias': materias_inscriptas})

def lista_materias_admin(request):
    carreras = Carrera.objects.all()
    materias_all = Materia.objects.all().order_by('anio')  
    query_carrera = request.GET.get('carrera')
    query_anio = request.GET.get('anio')
    filters = Q()
    
    if query_carrera:
        filters &= Q(carrera__id=query_carrera)

    if query_anio:
        filters &= Q(anio=query_anio)

    if filters:
        materias_all = materias_all.filter(filters)

    paginator = Paginator(materias_all, 10)
    page = request.GET.get('page')
    try:
        materias = paginator.page(page)
    except PageNotAnInteger:
        materias = paginator.page(1)
    except EmptyPage:
        materias = paginator.page(paginator.num_pages)
    
    return render(request, 'materias/lista_materias_admin.html', {'materias': materias, 'carreras': carreras})    

def alta_materia(request):
    if request.method == 'POST':
        form = MateriaForm(request.POST)
        if form.is_valid():
           form.save()
           return redirect('exito_alta_materia')
          
    else:
        form = MateriaForm()
        print(form)
    return render(request, 'materias/alta_materia.html', {'form': form})


def exito_cambios_materia(request):
    return render(request, 'materias/exito_cambios_materia.html')

def exito_alta_materia(request):
    return render(request, 'materias/exito_alta_materia.html')
def alerta_materia_existente(request):
    return render(request, 'alerta_materia_existente')

def listarMateriasFinal(request):
    materias_final = []
    materias_disponibles=usuarios_materia.objects.filter(usuario=request.user,aprobada=False)
    for m in materias_disponibles:
        if m.puede_inscribirse_en_mesa_final() and MesaFinal.objects.filter(materia=m.materia,vigente=True).exist():
            for mf in MesaFinal.objects.filter(materia=m.materia,vigente=True):
                materias_final.append(mf)
    return render(request, 'listarMateriasFinal.html', {'materias_final' : materias_final})

def altaMesa(request):
    if request.method == 'POST':
        form = MesaFinalForm(request.POST)
        fecha_llamado_str = request.POST.get('llamado')
        fecha_llamado = datetime.strptime(fecha_llamado_str, '%Y-%m-%d').date()
        fecha_actual = timezone.now().date()
        print(fecha_llamado)
        print(fecha_actual)
        if form.is_valid():
            if fecha_llamado > fecha_actual:
                form.save()
                return redirect('list_mesa')  # Redirige a la lista de mesas finales
            else:
                return JsonResponse({'status': 'error', 'message': 'La fecha de llamado debe ser posterior a la fecha de hoy'})  

    else:
        form = MesaFinalForm()
    return render(request, 'finales/alta_mesa_final.html', {'form': form})

def lista_finales_user(request):
    usuario = request.user.id
    finales_disponibles = []
    finales = MesaFinal.objects.all()
    for final in finales:
        if validar_inscripcion_final(usuario, final.materia.id) and final.inscripcionAbierta and InscripcionFinal.objects.filter(usuario=usuario, llamado__materia_id=final.materia.id).count()<1:
            print(final.materia)
            print(validar_inscripcion_final(usuario, final.materia.id))
            finales_disponibles.append(final)
    return render(request, 'finales/lista_finales_disponibles_user.html', {'finales': finales_disponibles})

def lista_finales_inscriptos_user(request):
    usuario = request.user.id
    finales_inscriptos = InscripcionFinal.objects.filter(
        usuario_id=usuario,
        aprobada=None
    )
    return render(request, 'finales/lista_finales_inscriptos_user.html', {'finales': finales_inscriptos})

def lista_finales_inscriptos_adm(request):
    finales_inscriptos = InscripcionFinal.objects.filter(
        Q(aprobada=False) | Q(aprobada__isnull=True)
    ).select_related('llamado__materia', 'usuario')
    for final in finales_inscriptos:
        final.notas = usuarios_materia.objects.filter(
            usuario=final.usuario,
            materia=final.llamado.materia
    )
    return render(request, 'finales/lista_finales_inscriptos_adm.html', {'finales': finales_inscriptos})

def inscripcionMesa(request):
    if request.method == 'POST':
        form = InscripcionFinalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finales/inscripcion_final.html')  # Redirige a la página de éxito de inscripción
    else:
        form = InscripcionFinalForm()
    return render(request, 'finales/inscripcion_final.html', {'form': form})

def exito_inscripcion_final(request):
    return render(request, 'finales/exito_inscripcion_final.html')

################################################################
def inscripcionFinal(request):
    if request.method == 'POST':
        final_usuario=request.POST['usuario']
        final_llamado=request.POST['llamado']
        usuario= get_object_or_404(Usuario,id=final_usuario)
        form = InscripcionFinalForm(request.POST)
        final = get_object_or_404(MesaFinal, id=final_llamado)
        try:
            inscripcion_materia = get_object_or_404(usuarios_materia, usuario_id=final_usuario,materia_id__nombre_materia=final.materia)
        except:
            pass
        if form.is_valid():
            try:
                if inscripcion_materia.nota_final is None or inscripcion_materia.nota_final < 4:
                    if InscripcionFinal.objects.filter(usuario=final_usuario, llamado__materia=final.materia).count()<1:
                        if usuarios_materia.objects.filter(usuario=final_usuario,materia=final.materia).count()==1:
                            form.save()
                            return JsonResponse({'status': 'success', 'message': str(usuario.nombre_completo) + ' se inscribio correctamente al final de '+ str(final.materia.nombre_materia)})  # Redirige a pagina de exito de alta de mesa
                        else:
                            return JsonResponse({'status': 'nose', 'message': str(usuario.nombre_completo) + ' no se encuentra inscripto a la materia '+ str(final.materia.nombre_materia)})  
                    else:
                        return JsonResponse({'status': 'duplicado', 'message': str(usuario.nombre_completo) + ' ya está inscripto a una mesa de final de '+ str(final.materia.nombre_materia)})           
                else:
                    return JsonResponse({'status': 'nose', 'message': str(usuario.nombre_completo) + ' ya aprobó el final de ' + str(final.materia.nombre_materia) + ' con nota ' + str(inscripcion_materia.nota_final)})
            except:
                if InscripcionFinal.objects.filter(usuario=final_usuario, llamado__materia=final.materia).count()<1:
                    if usuarios_materia.objects.filter(usuario=final_usuario,materia=final.materia).count()==1:
                        form.save()
                        return JsonResponse({'status': 'success', 'message': str(usuario.nombre_completo) + ' se inscribio correctamente al final de '+ str(final.materia.nombre_materia)})  # Redirige a pagina de exito de alta de mesa
                    else:
                        return JsonResponse({'status': 'nose', 'message': str(usuario.nombre_completo) + ' no se encuentra inscripto a la materia '+ str(final.materia.nombre_materia)})  
                else:
                    return JsonResponse({'status': 'duplicado', 'message': str(usuario.nombre_completo) + ' ya está inscripto a una mesa de final de '+ str(final.materia.nombre_materia)})           
    else:
        form = InscripcionFinalForm()
    return render(request, 'finales/inscripcion_final_adm.html',  {'form': form}) 

def inscripcionFinalEst(request, final_id):
    final = get_object_or_404(MesaFinal, id=final_id)
    
    if request.method == 'GET':
        inscripcion_usuario = request.user
        
        # Verificar si ya existe la inscripción
        if InscripcionFinal.objects.filter(usuario=inscripcion_usuario, llamado=final).exists():
            messages.warning(request, 'Ya estás inscrito en este final.')
            return redirect('/inscripcionFinalEst/')
        
        # Validar la inscripción
        if validar_inscripcion_final(inscripcion_usuario.id, final.materia):
            # Crear el objeto InscripcionFinal
            nueva_inscripcion = InscripcionFinal(
                usuario=inscripcion_usuario,
                llamado=final,
            )
            nueva_inscripcion.save()
            
            messages.success(request, 'Te has inscrito exitosamente en el final.')
            return redirect('/inscripcionFinalEst/')
        else:
            messages.error(request, 'No cumples con los requisitos para inscribirte en este final.')
            return redirect('/inscripcionFinalEst/')
    
    # Si es GET, mostrar el formulario de confirmación
    return render(request, 'finals/inscripcion_final_adm.html', {'final': final})

def inscripcionMateria(request):
    if request.method == 'POST':
        inscripcion_usuario=request.POST['usuario']
        inscripcion_materia=request.POST['materia']
        form = InscripcionMateriaForm(request.POST)
        if form.is_valid():
            if usuarios_materia.objects.filter(usuario=inscripcion_usuario, materia=inscripcion_materia).count()<1:
                form.save()
                return redirect('exito_inscripcion_mesa')  # Redirige a pagina de exito de alta de mesa
            else:
                return redirect('error_inscripcion_adm')             
    else:
        form = InscripcionMateriaForm()
    return render(request, 'materias/inscripcion_materia_adm.html',  {'form': form}) 

def inscripcionMateriaEst(request, materia_id,modalidad):
    materia = get_object_or_404(Materia, id=materia_id)
    
    if request.method == 'GET':
        inscripcion_usuario = request.user
        
        # Verificar si ya existe la inscripción
        if usuarios_materia.objects.filter(usuario=inscripcion_usuario, materia=materia).exists():
            messages.warning(request, 'Ya estás inscrito en esta materia.')
            return redirect('/inscripcionMateriaEst')
        
        # Validar la inscripción
        if validar_inscripcion_materias(inscripcion_usuario.id, materia_id):
            # Crear el objeto usuarios_materia
            nueva_inscripcion = usuarios_materia(
                usuario=inscripcion_usuario,
                materia=materia,
                modalidad=modalidad
            )
            nueva_inscripcion.save()
            
            messages.success(request, 'Te has inscrito exitosamente en la materia.')
            return redirect('/inscripcionMateriaEst')
        else:
            messages.error(request, 'No cumples con los requisitos para inscribirte en esta materia.')
            return redirect('/inscripcionMateriaEst')
    
    # Si es GET, mostrar el formulario de confirmación
    return render(request, 'materias/inscripcion_materia_est.html', {'materia': materia})

def exito_inscripcion_mesa(request):
    return render(request, 'finales/exito_inscripcion_mesa.html')

def error_alta_mesa(request):
    return render(request, 'finales/error_alta_mesa.html')

def exito_alta_mesa(request):
    return render(request, 'finales/exito_alta_mesa.html')

def error_inscripcion_adm(request):
    return render(request, 'finales/error_inscripcion_adm.html')

def error_inscripcion_est(request):#No tenes la nota de cursada minima
    return render(request, 'finales/error_inscripcion_est.html')
def error_inscripcion_est1(request):#No tenes la nota de cursada minima
    return render(request, 'finales/error_inscripcion_est1.html')
def error_inscripcion_est2(request):#Ya tenes nota de final no te podes volver a inscribir
    return render(request, 'finales/error_inscripcion_est2.html')
def error_inscripcion_est3(request):#No estas inscripto a la materia
    return render(request, 'finales/error_inscripcion_est3.html')
def error_inscripcion_est5(request):#No aprobaste la correlativa
    return render(request, 'finales/error_inscripcion_est5.html')
def error_inscripcion_est6(request):#No cursaste la correlativa
    return render(request, 'finales/error_inscripcion_est6.html')
    
################################################################

#Nico y Cami were here

def crear_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = EstudianteForm()
    return render(request, 'crear_estudiante.html', {'form':form})

def crear_profesor(request):
    if request.method =='POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ProfesorForm()
        return render(request, 'crear_profesor.html', {'form':form})
    

def crear_preceptor(request):
    if request.method =='POST':
        form = PreceptorForm(request.Post)
        if form.is_valid():
            form.save()
    else:
        form = PreceptorForm()
        return render(request, 'crear_preceptor.html',{'form':form})
    

def crear_Directivo(request):
    if request.method =='POST':
        form = DirectivoForm(request.Post)
        if form.is_valid():
            form.save()
    else:
        form = DirectivoForm()
        return render(request, 'crear_directivo.html',{'form':form})
    
    
class EstudianteCreateView(CreateView):
    model = Estudiante
    fields = ['username', 'password', 'matricula', ]
    template_name = 'estudiante_form.html'
    success_url = reverse_lazy('estudiante_lista')

class EstudianteUpdateView(UpdateView):
    model = Estudiante
    fields = ['username', 'matricula',]
    template_name = 'estudiante.form.html'
    success_url = reverse_lazy('estudiante_lista')

class EstudianteDeleteView(DeleteView):
    model = Estudiante
    template_name = 'confirmar_eliminar_estudiante.html'
    success_url = reverse_lazy('estudiante_lista')
    


def cargar_usuarios(request):
    if request.method == 'POST':
        formulario = ArchivoForm(request.POST, request.FILES)
        if formulario.is_valid():
            archivo_csv = request.FILES['csv_file']
            decoded_file = archivo_csv.read().decode('latin1').splitlines()
            archivo_csv = csv.DictReader(decoded_file,delimiter=';')
            flagDuplicado=0
            for fila in archivo_csv:
                try:
                    email = fila['Correo electrónico']
                    nombre_completo = fila['Nombre estudiante']
                    dni = fila['Documento estudiante']
                    username = dni
                    password = dni
                    matricula = dni
                    usuario = Estudiante.objects.create_user(email=email,nombre_completo=nombre_completo,rol='Estudiante', dni=dni,username=username, password=password, matricula=matricula)                
                except:
                    pass
                    flagDuplicado=1
            if flagDuplicado==0:
                return render(request,'registration/exito_carga_masiva.html')
            else:
                return render(request,'registration/warning_carga_masiva.html')
    else:
        formulario = ArchivoForm()

    return render(request, 'registration/cargar_usuarios.html', {'formulario': formulario})

def alta_masiva_materia(request):
    if request.method == 'POST' and request.Files['archivo_csv']:
        archivo_csv = request.FILES['archivo_csv']
        decoded_file = archivo_csv.read().decode('utf-8').splitlines() 
        archivo_csv= csv.DictReader(decoded_file) 

        for fila in archivo_csv:
            nombre = fila['nombre']
            profesor = fila['profesor']
            carrera = fila ['carrera']
        return HttpResponse ('Materias importadas correctamente')
    return render(request, 'alta_masiva_materia.html') 
    
def editar_materia(request, id):
    materia = get_object_or_404(Materia, id=id)
    if request.method == 'POST':
        form = MateriaForm(request.POST, instance=materia)
        if form.is_valid():
            form.save()
            return redirect('exito_cambios_materia')
    else:
        form = MateriaForm(instance=materia)
        return render(request, 'materias/editar_materia.html', {'form': form})


    
def eliminar_materia(request, id):
    materia = get_object_or_404(Materia, pk=id)
    if request.method == 'POST':
        materia.delete()
        return redirect('exito_materia_eliminada_adm')
    return render(request, 'materias/eliminar_materia.html', {'materia': materia})

def eliminar_mesa(request, id):
    mesa = get_object_or_404(MesaFinal, pk=id)
    if request.method == 'POST':
        mesa.delete()
        return redirect('exito_mesa_eliminada')
    return render(request, 'mesas/eliminar_mesa.html', {'mesa': mesa})

def eliminar_inscripcion_final(request, id):
    final = get_object_or_404(InscripcionFinal, pk=id)
    if request.user.id==final.usuario_id and not request.user.is_staff and not request.user.is_superuser:
        if request.method == 'POST':
            final.delete()
            return redirect('exito_final_eliminado_est')
        return render(request, 'finales/eliminar_final_est.html', {'final': final})
    elif request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            final.delete()
            return redirect('exito_final_eliminado_adm')
        return render(request, 'finales/eliminar_final_est.html', {'final': final})        
    else:
        return render(request,'403_forbidden.html')

def eliminar_materias_seleccionadas(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            materia_ids = request.POST.getlist('materia_ids')
            cantidad_eliminadas = len(materia_ids)
            print(request.POST)
            if cantidad_eliminadas > 0:
                Materia.objects.filter(id__in=materia_ids).delete()
            materias = Materia.objects.all()
            return render(request, 'materias/lista_materias_admin.html', {'materias': materias, 'cantidad_eliminadas': cantidad_eliminadas})
        return redirect("lista_materias_admin")
    elif not request.user.is_staff or not request.user.is_superuser:
        return render(request,'403_forbidden.html')
    
def abrir_materias_seleccionadas(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            materia_ids = request.POST.getlist('materia_ids')
            cantidad_eliminadas = len(materia_ids)
            print(request.POST)
            if cantidad_eliminadas > 0:
                Materia.objects.filter(id__in=materia_ids).update(inscripcionAbierta=True)
            return redirect(reverse_lazy('lista_materias_admin'))
        else:
            return redirect(reverse_lazy('lista_materias_admin'))
    elif not request.user.is_staff or not request.user.is_superuser:
        return render(request,'403_forbidden.html')

def cerrar_materias_seleccionadas(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            materia_ids = request.POST.getlist('materia_ids')
            cantidad_eliminadas = len(materia_ids)
            print(request.POST)
            if cantidad_eliminadas > 0:
                Materia.objects.filter(id__in=materia_ids).update(inscripcionAbierta=False)
            return redirect(reverse_lazy('lista_materias_admin'))
        else:
            return redirect(reverse_lazy('lista_materias_admin'))
    elif not request.user.is_staff or not request.user.is_superuser:
        return render(request,'403_forbidden.html')
    
def eliminar_mesas_seleccionadas(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            mesa_ids = request.POST.getlist('mesa_ids')
            cantidad_eliminadas = len(mesa_ids)
            if cantidad_eliminadas > 0:
                MesaFinal.objects.filter(id__in=mesa_ids).delete()
            mesas = MesaFinal.objects.all()
            return redirect('/mesas_lista')
        return redirect('/mesas_lista')
    elif not request.user.is_staff or not request.user.is_superuser:
        return render(request,'403_forbidden.html')
    
def abrir_mesas_seleccionadas(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            mesa_ids = request.POST.getlist('mesa_ids')
            cantidad_eliminadas = len(mesa_ids)
            print(request.POST)
            if cantidad_eliminadas > 0:
                MesaFinal.objects.filter(id__in=mesa_ids).update(inscripcionAbierta=True)
            mesas = MesaFinal.objects.all()
            return redirect('/mesas_lista')
        return redirect('/mesas_lista')
    elif not request.user.is_staff or not request.user.is_superuser:
        return render(request,'403_forbidden.html')
    
def cerrar_mesas_seleccionadas(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            mesa_ids = request.POST.getlist('mesa_ids')
            cantidad_eliminadas = len(mesa_ids)
            print(request.POST)
            if cantidad_eliminadas > 0:
                MesaFinal.objects.filter(id__in=mesa_ids).update(inscripcionAbierta=False)
            mesas = MesaFinal.objects.all()
            return redirect('/mesas_lista')
        return redirect('/mesas_lista')
    elif not request.user.is_staff or not request.user.is_superuser:
        return render(request,'403_forbidden.html')

#def eliminar_inscripcion_materia(request, id):
#    materia = get_object_or_404(usuarios_materia, pk=id)
#    if request.user.id==materia.usuario_id and not request.user.is_staff and not request.user.is_superuser:
#        if request.method == 'POST':
#            materia.delete()
#            return redirect('exito_materia_eliminada_est')
#        return render(request, 'materias/eliminar_materia_est.html', {'materia': materia})
#    elif request.user.is_staff or request.user.is_superuser:
#        if request.method == 'POST':
#            materia.delete()
#            return redirect('exito_materia_eliminada_adm')
#        return render(request, 'materias/eliminar_materia_est.html', {'materia': materia})        
#    else:
#        return render(request,'403_forbidden.html')
    
def eliminar_inscripcion_materia(request, id):
    materia = get_object_or_404(usuarios_materia, pk=id)
    
    if request.user.id == materia.usuario_id and not request.user.is_staff and not request.user.is_superuser:
        if request.method == 'POST':
            # Eliminar inscripciones a finales relacionadas
            InscripcionFinal.objects.filter(
                Q(usuario=request.user) & Q(llamado__materia=materia.materia)
            ).delete()
            
            # Eliminar la inscripción a la materia
            materia.delete()
            return redirect('exito_materia_eliminada_est')
        return render(request, 'materias/eliminar_materia_est.html', {'materia': materia})
    
    elif request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            # Eliminar inscripciones a finales relacionadas
            InscripcionFinal.objects.filter(
                Q(usuario=materia.usuario) & Q(llamado__materia=materia.materia)
            ).delete()
            
            # Eliminar la inscripción a la materia
            materia.delete()
            return redirect('exito_materia_eliminada_adm')
        return render(request, 'materias/eliminar_materia_est.html', {'materia': materia})
    
    else:
        return render(request, '403_forbidden.html')

def exito_materia_eliminada(request):
    return render(request, 'materias/exito_materia_eliminada.html')

def exito_materia_eliminada_adm(request):
    return render(request, 'materias/exito_materia_eliminada_adm.html')

def exito_materia_eliminada_est(request):
    return render(request, 'materias/exito_materia_eliminada_est.html')

def exito_final_eliminado_est(request):
    return render(request, 'finales/exito_final_eliminado_est.html')

def exito_final_eliminado_adm(request):
    return render(request, 'finales/exito_final_eliminado_adm.html')

def ver_materias(request, id):
    materia = get_object_or_404(Materia, pk=id)
    return render(request, 'materias/ver_materia.html', {'materia': materia})

def cambiar_contraseña (request):
    if request.method == 'POST':
        
        username = User.objects.get(username='username')
        
        contraseña_nueva = request.POST['contraseña_nueva']
        
        username.set_password(contraseña_nueva)
        
        username.save()
        
        return HttpResponse('Su contraseña se cambio con exito')
    else : 
        return render(request, 'registration/change_password.html')  
    
  
def alta_estudiante(request):
        if request.method == 'POST' :
            form = EstudianteForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect (request, 'alta_exitosa.html')
        else:
            form = EstudianteForm()
            return render(request, 'alta_estudiante.html', {'form': form})
        
class MesasFinalesListView(ListView):
    model = MesaFinal
    template_name = 'finales/mesas_finales_list.html'
    context_object_name = 'mesas_finales'

def inscribir_mesa_final(request):
    if request.method == 'POST':
        filtro_form = FiltroInscripcionForm(request.POST)
        if filtro_form.is_valid():
            estudiante = filtro_form.cleaned_data.get('estudiante')
            materia = filtro_form.cleaned_data.get('materia')
            # Agrega lógica para filtrar según estudiante y/o materia
            mesas_finales = MesaFinal.objects.filter(materia__nombre__icontains=materia,inscripcionfinal__usuario__nombre__icontains=estudiante)
        else:
            mesas_finales = MesaFinal.objects.all()
    else:
        filtro_form = FiltroInscripcionForm()
        mesas_finales = MesaFinal.objects.all()

    context = {'mesas_finales': mesas_finales, 'filtro_form': filtro_form}
    return render(request, 'finales/inscribir_mesa_final.html', context)

def listar_usuarios_materia(request):
    usuarios_materia_data = usuarios_materia.objects.all()  # Recupera todos los registros de usuarios_materia
    context = {'usuarios_materia_data': usuarios_materia_data}
    return render(request, 'registration/ver_usuarios_materia.html', context)


def validar_inscripcion_final(usuario_id, materia_id):
    # Verificamos si el usuario está inscrito a la materia y su nota de cursada
    try:
        usuario_materia_instance = usuarios_materia.objects.get(
            usuario_id=usuario_id,  # Ajusta si el campo es diferente
            materia_id=materia_id   # Ajusta si el campo es diferente
        )
        nota_cursada = usuario_materia_instance.nota_cursada
        nota_final = usuario_materia_instance.nota_final
        
        if nota_cursada is None or nota_cursada < 7:
            return False
            #JsonResponse({
            #    'puede_inscribirse': False,
            #    'mensaje': 'No tienes la nota de cursada mínima (7) para inscribirte al final.'
            #})
        
        if nota_final is not None:
            return False
            #JsonResponse({
            #    'puede_inscribirse': False,
            #    'mensaje': 'Ya tienes una nota de final registrada para esta materia. No puedes inscribirte nuevamente.'
            #})
    except usuarios_materia.DoesNotExist:
        return False 
        #JsonResponse({
        #    'puede_inscribirse': False,
        #    'mensaje': 'No estás inscrito a esta materia.'
        #})

    # Obtenemos todas las materias correlativas de la materia a la que se quiere inscribir
    correlativas = MateriaCorrelativa.objects.filter(materia_id=materia_id)
    
    # Si no hay correlativas, el usuario puede inscribirse directamente
    if not correlativas.exists():
        return True
        #JsonResponse({
        #    'puede_inscribirse': True,
        #    'mensaje': 'Puedes inscribirte a la mesa final. Esta materia no tiene correlativas.'
        #})

    # Si hay correlativas, verificamos si el usuario ya aprobó todas
    for correlativa in correlativas:
        try:
            correlativa_instance = usuarios_materia.objects.get(
                usuario_id=usuario_id,  # Ajusta si el campo es diferente
                materia_id=correlativa.materia_correlativa_id  # Ajusta si el campo es diferente
            )
            print(correlativa_instance.nota_final)
            
            nota_final = correlativa_instance.nota_final
            if nota_final is None or nota_final < 4:
                return False
                #return JsonResponse({
                #    'puede_inscribirse': False,
                #    'mensaje': f'No has aprobado la materia correlativa {correlativa.materia_correlativa.nombre_materia} con nota 4 o superior.'
                #})
        except usuarios_materia.DoesNotExist:
            print("Nodeberiaperounonuncasabe")
            return False
        #JsonResponse({
        #        'puede_inscribirse': False,
        #        'mensaje': f'No has cursado la materia correlativa {correlativa.materia_correlativa.nombre_materia}.'
        #    })
    
    # Si llegamos aquí, el usuario puede inscribirse
    return True
#JsonResponse({
#        'puede_inscribirse': True,
#        'mensaje': 'Puedes inscribirte a la mesa final.'
#    })

def validar_inscripcion_materias(usuario_id, materia_id):
    try:
        # Verificamos si el usuario está inscrito a la materia
        usuarios_materia.objects.get(
            usuario_id=usuario_id,
            materia_id=materia_id
        )
        return False  # Ya estás inscrito a la materia
    except usuarios_materia.DoesNotExist:
        # El usuario no está inscrito, continuamos con la validación
        pass

    # Obtenemos todas las materias correlativas de la materia a la que se quiere inscribir
    correlativas = MateriaCorrelativa.objects.filter(materia_id=materia_id)

    if not correlativas.exists():
        return True #Se puede inscribir, no hay correlativas
    for correlativa in correlativas:
        try:
            correlativa_instance = usuarios_materia.objects.get(
                usuario_id=usuario_id,
                materia_id=correlativa.materia_correlativa_id  
            )
            
            nota_final = correlativa_instance.nota_final
            if nota_final is None or nota_final < 4:
                return False #No se aprobó final de la correlativa
        except usuarios_materia.DoesNotExist:
            return False #No se curso correlativa
    return True #Se puede inscribir



def inscribir_usuario(usuario, materia):
    # Verificar si ya existe una inscripción para este usuario y materia
    inscripcion, created = InscripcionFinal.objects.get_or_create(
        Usuario=usuario,
        Materia=materia,
        defaults={
            'Fecha_Inscripcion': timezone.now()
        }
    )
    
    if not created:
        # Si la inscripción ya existía, actualizamos la fecha de inscripción
        inscripcion.Fecha_Inscripcion = timezone.now()
        inscripcion.save()

def cargar_nota_final(request, inscripcion_id):
    inscripcion = get_object_or_404(InscripcionFinal, id=inscripcion_id)
    usuario_materia = get_object_or_404(usuarios_materia, usuario=inscripcion.usuario, materia=inscripcion.llamado.materia)

    if request.method == 'POST':
       form = NotaFinalForm(request.POST)
       if form.is_valid():
            nota_final = form.cleaned_data['nota_final']
            usuario_materia.nota_final = nota_final
            usuario_materia.aprobada = nota_final >= 4
            usuario_materia.save()
            inscripcion.aprobada = nota_final >= 4
            inscripcion.save()

            print(f"Nota final: {nota_final}")
            print(f"Aprobada: {inscripcion.aprobada}")

            messages.success(request, f'Nota final cargada correctamente: {nota_final}')
            return redirect('/listaFinalesAdm')  # Ajusta esto a tu URL de redirección
    else:
        form = NotaFinalForm()

    context = {
        'form': form,
        'inscripcion': inscripcion,
        'usuario_materia': usuario_materia,
    }
    return render(request, 'finales/cargar_nota.html', context)

def cargar_nota_cursada(request,id):
    usuario_materia = get_object_or_404(usuarios_materia, id=id)

    if request.method == 'POST':
        form = NotaCursadaForm(request.POST)
        if form.is_valid():
            nota_cursada = form.cleaned_data['nota_cursada']
            usuario_materia.nota_cursada = nota_cursada
            usuario_materia.save()

            messages.success(request, f'Nota de cursada cargada correctamente: {nota_cursada}')
            return redirect('/listaMateriasAdm')  # Ajusta esto a tu URL de redirección
    else:
        form = NotaCursadaForm()

    context = {
        'form': form,
        'usuarios_materia': usuario_materia,
    }
    return render(request, 'materias/cargar_nota.html', context)

def editar_notas(request, id):
    usuario_materia = get_object_or_404(usuarios_materia, id=id)

    if request.method == 'POST':
        form = NotaCursadaForm(request.POST, instance=usuario_materia)
        if form.is_valid():
            form.save()
            return redirect('/listaMateriasAdm/')
    else:
        form = NotaCursadaForm(instance=usuario_materia)
    
    return render(request, 'materias/cargar_nota.html', {'form': form})

def abrir_inscripcion_materia(request,carrera,anio):
    if request.user.is_staff or request.user.is_superuser:
        Materia.objects.filter(carrera_id=carrera,anio=anio).update(inscripcionAbierta=True)
        return redirect('lista_materias_admin')
    else:
        return render(request,"403_forbidden.html")

def cerrar_inscripcion_materia(request,carrera,anio):
    if request.user.is_staff or request.user.is_superuser:
        Materia.objects.filter(carrera_id=carrera,anio=anio).update(InscripcionAbierta=False)
        return redirect('lista_materias_admin')
    else:
        return render(request,"403_forbidden.html")
    
def eliminar_usuarios(request, usuario_id=None):
    # Restricciones de acceso
    if not (request.user.is_staff or request.user.is_superuser or request.user.admin):
        return render(request, 'registration/error403.html', {'error_message': "No tienes permiso para realizar esta acción."})
    if request.method == 'POST':
        if usuario_id:
            # Eliminar un solo usuario
            if str(request.user.id) == usuario_id:
                return render(request, 'registration/error403.html', {'error_message': "No puedes eliminar tu propio usuario."})
            
            usuario = get_object_or_404(Usuario, pk=usuario_id)
            usuario.delete()
            return redirect('list_user', cantidad_eliminadas=1)
        else:
            # Eliminar múltiples usuarios
            usuarios_ids = request.POST.getlist('usuarios_ids')
            if str(request.user.id) in usuarios_ids:
                return render(request, '403_forbidden.html', {'error_message': "No puedes eliminar tu propio usuario."})
            cantidad_eliminadas = len(usuarios_ids)
            if cantidad_eliminadas > 0:
                Usuario.objects.filter(id__in=usuarios_ids).delete()
            return redirect('list_user')
    
    return redirect('list_user')
    
class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('recover_pass.html')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'
    

def acta_volante(request, final_id):

    pages = []
    finales_inscriptos = InscripcionFinal.objects.filter(llamado=final_id).order_by('usuario__nombre_completo')
    final = get_object_or_404(MesaFinal, id=final_id)
    if finales_inscriptos.count()<=25:
        context = {
            'finales_inscriptos': finales_inscriptos,
            'final': final,
            'cant_inscriptos': finales_inscriptos.count(),
            'piso':0
        }
        return render(request, 'finales/acta_volante.html', context)
    else:
        for i in range(1,ceil(finales_inscriptos.count()/25)+1):
            inscriptos = []
            for inscripto in range(25*(i-1),25*(i-1)+25):
                print(inscripto)
                try:
                    inscriptos.append(finales_inscriptos[inscripto])
                except:
                    pass
            context = {
                'finales_inscriptos': inscriptos,
                'final': final,
                'cant_inscriptos': finales_inscriptos.count(),
                'piso':25*(i-1),
            }
            print(f"fin {i} pagina")
            html = render(request, 'finales/acta_volante.html', context).content.decode('utf-8')
            pages.append({
                'id':f'page_{i}',
                'title':f'Acta volante {i}: {final.materia}',
                'content':html
            })
        pages_json = dumps(pages)
        return render(request, 'finales/lista_acta_volante.html', {'pages_json': pages_json})

def reporte_usuario_materias(request, usuario_id):

    try:
        usuario = Usuario.objects.get(id=usuario_id)
        print(usuario.id)
    except Usuario.DoesNotExist:    
        return HttpResponse("Usuario no encontrado", status=404)
    
    carrera = usuario.carrera 
    # materias_de_carrera = usuarios_materia.objects.filter(carrera = usuario.carrera) #hace falta el total de materias de la carrera, no sólo las inscripciones
    if not carrera:
        return HttpResponse("El usuario no tiene carreras registradas", status=404)

    # Aquí asumimos que solo tomamos la primera carrera, en caso que esté inscripto en más de una carrera
    #carrera = carreras.first()
    # Acceder al número de resolución de la carrera
    #num_resolucion = carrera.num_resolucion if carrera else None

    materias_data = usuarios_materia.objects.filter(usuario=usuario, aprobada=True).values(
        'materia__nombre_materia', 'nota_cursada', 'nota_final', 'materia__anio'
    )
    #total_materias = usuarios_materia.objects.filter(carrera=carrera).count()
    materias_aprobadas = len(materias_data)
    #porcentaje_aprobado = (materias_aprobadas / total_materias) * 100 if total_materias > 0 else 0
   
    materias_por_anio = {}
    for materia in materias_data:
        anio = materia['materia__anio']
        if anio not in materias_por_anio:
            materias_por_anio[anio] = []
        materias_por_anio[anio].append(materia)

     # Obtener la fecha actual para el pie del informe
    fecha_actual = datetime.now()
    dia = fecha_actual.day
    mes = fecha_actual.strftime("%B")  # Nombre del mes
    año = fecha_actual.year

    context = {
        'usuario': usuario,
        'materias_por_anio': materias_por_anio,
       # 'porcentaje_aprobado': porcentaje_aprobado,
       # 'resolucion': usuarios_carreras.num_resolucion,
        'fecha_dia': dia,
        'mes': mes,
        'año': año,
    }
    template = loader.get_template('materias/reporte_usuario_materias.html/')
    html = template.render(context)

    # Convertir HTML a PDF utilizando WeasyPrint con estilos CSS
    css = CSS(string='@page { size: A4; margin: 2cm }')  # Define el tamaño del papel y márgenes
    pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[css])

#    Generar la respuesta HTTP
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=reporte_usuario_{usuario.nombre_completo}.pdf'
    return response



def reporte_estudiante(request, usuario_id):
    materias_aprobadas = usuarios_materia.objects.filter(usuario_id=usuario_id, aprobada=True).count()
    print(materias_aprobadas)
    hoy = timezone.now().date()
    usuario = get_object_or_404(Usuario, id=usuario_id)
    carrera = get_object_or_404(Carrera, nombre_carrera="Tecnicatura Superior en Analisis de Sistemas")
    # Prefetch para optimizar las consultas
    usuarios_materia_prefetch = Prefetch(
        'usuarios_materia_set',  # Cambiado de 'usuarios_materia' a 'usuarios_materia_set'
        queryset=usuarios_materia.objects.filter(usuario_id=usuario_id),
        to_attr='usuario_materia'
    )
    materias_primero = Materia.objects.filter(anio=1).prefetch_related(usuarios_materia_prefetch).order_by('nombre_materia')
    materias_segundo = Materia.objects.filter(anio=2).prefetch_related(usuarios_materia_prefetch).order_by('nombre_materia')
    materias_tercero = Materia.objects.filter(anio=3).prefetch_related(usuarios_materia_prefetch).order_by('nombre_materia')
    cant_materias = Materia.objects.count()
    # Procesamiento de las materias y sus notas
    def procesar_materias(materias):
        return [
            {
                'materia': materia,
                'nota_final': next((um.nota_final for um in materia.usuario_materia if um.usuario_id == usuario_id), "-"),
                'nota_texto': numero_a_texto(next((um.nota_final for um in materia.usuario_materia if um.usuario_id == usuario_id), "-"))
            }
            for materia in materias
        ]
    materias_primero_con_notas = procesar_materias(materias_primero)
    materias_segundo_con_notas = procesar_materias(materias_segundo)
    materias_tercero_con_notas = procesar_materias(materias_tercero)
    if cant_materias > 0:
        porcentaje = round((materias_aprobadas / cant_materias)*100, 2)
    else:
        porcentaje = 0
    context = {
        'usuario': usuario,
        'porcentaje_aprobado': porcentaje,
        'materias_primero': materias_primero_con_notas,
        'materias_segundo': materias_segundo_con_notas,
        'materias_tercero': materias_tercero_con_notas,
        'carrera': carrera,
        'fecha':hoy
    }
    return render(request, 'registration/reporte_estudiante.html', context)

def numero_a_texto(numero):
    if numero != '-' and numero is not None:
        unidades = ['', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve']
        decenas = ['diez', 'once', 'doce', 'trece', 'catorce', 'quince', 'dieciséis', 'diecisiete', 'dieciocho', 'diecinueve']
        decenas_completas = ['', '', 'veinte', 'treinta', 'cuarenta', 'cincuenta', 'sesenta', 'setenta', 'ochenta', 'noventa']

        def convertir_entero(n):
            if n < 10:
                return unidades[n].capitalize()
            elif n < 20:
                return decenas[n-10].capitalize()
            elif n < 100:
                if n % 10 == 0:
                    return decenas_completas[n // 10].capitalize()
                else:
                    return f"{decenas_completas[n // 10]} y {unidades[n % 10]}".capitalize()
            else:
                return "Cien"

        parte_entera = int(numero)
        parte_decimal = int(round((numero - parte_entera) * 100))

        texto_entero = convertir_entero(parte_entera)

        if parte_decimal == 0:
            return texto_entero
        else:
            texto_decimal = convertir_entero(parte_decimal)
            return f"{texto_entero} con {texto_decimal.lower()}"
    else:
        return "-"