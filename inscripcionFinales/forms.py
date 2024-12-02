import csv
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.forms import DateInput
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
#from django.forms import ModelForm, CustomPasswordChangeForm
from .models import *

validador= RegexValidator(r'^[0-9]*$','Solo se permiten números')
class institutoForms(forms.ModelForm):
      nombre_instituto = forms.CharField(max_length=30)
      email = forms.CharField(max_length=20)
      class Meta:
            model = Instituto
            fields = (
            'nombre_instituto',
            'email_instituto',
            'direccion',
            'localidad',
            'ciudad',
            )


class carreraForm(forms.ModelForm):
      nombre_carrera = forms.CharField( max_length=100)
      num_resolucion = forms.CharField(max_length=100)
      class Meta:
        model = Carrera
        fields =(
          'nombre_carrera',
          'num_resolucion',
          'duracion_carrera',
          'instituto',

        )

class usuarios_materiaForm(forms.ModelForm):
      nombre_materia = forms.CharField( max_length=100)
      class Meta:
        model = Materia
        fields =(
          'nombre_materia',
          'carrera',
          'profesor'

        )

class usuarios_materiaForm(forms.ModelForm):
      nombre_materia = forms.CharField( max_length=100)
      class Meta:
        model = Materia
        fields =(
          'nombre_materia',
          'carrera',
          'profesor'

        )

class materiaCorrelativaForm(forms.ModelForm):
      nombre_materiaCorrelativa = forms.CharField( max_length=100)
      class Meta:
        model = MateriaCorrelativa
        fields =(
          'materia',
          'materia_correlativa'
        )

class registri_user_form(UserCreationForm):
    email = forms.EmailField(required=True)
    dni = forms.CharField(max_length=15, validators=[validador])
    
    password1 = None
    password2 = None
    
    carrera = forms.ModelChoiceField(
        queryset=Carrera.objects.all(),
        empty_label="Seleccione una carrera"
    )
    especialidad = forms.CharField(max_length=100, required=False)
    cargo = forms.CharField(max_length=100, required=False)
    area = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Usuario
        fields = ['email', 'nombre_completo', 'dni', 'rol', 'carrera', 'especialidad', 'cargo', 'area']

    def clean(self):
        password = Usuario.objects.make_random_password(length=10,allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
        self.cleaned_data['password1'] = password
        self.cleaned_data['password2'] = password

        return super().clean()

    def save(self, commit=True):
        usuario = super().save(commit=False)
        rol = self.cleaned_data.get('rol', '').lower()
        print(usuario.dni)
        usuario.set_password(str(usuario.dni))
        if rol == 'Estudiante':
            estudiante = Estudiante.objects.create(
                email=usuario.email,
                nombre_completo=usuario.nombre_completo,
                dni=usuario.dni,
                rol=usuario.rol,
            )
            estudiante.carrera.set([self.cleaned_data['carrera']])
            usuario = estudiante
        elif rol == 'Profesor':
            usuario = Profesor.objects.create(
                email=usuario.email,
                nombre_completo=usuario.nombre_completo,
                dni=usuario.dni,
                rol=usuario.rol,
                especialidad=self.cleaned_data['especialidad']
            )
        elif rol == 'Directivo':
            usuario = Directivo.objects.create(
                email=usuario.email,
                nombre_completo=usuario.nombre_completo,
                dni=usuario.dni,
                rol=usuario.rol,
                cargo=self.cleaned_data['cargo']
            )
        elif rol == 'Preceptor':
            usuario = Preceptor.objects.create(
                email=usuario.email,
                nombre_completo=usuario.nombre_completo,
                dni=usuario.dni,
                rol=usuario.rol,
                area=self.cleaned_data['area']
            )
               
        usuario.save()
        return usuario



class profile_students_form(forms.ModelForm):   
  class Meta:
    model = Usuario
    fields = (
      'username',
      'nombre_completo',
      'fecha_nac',
      'dni',
      'direccion',
      'localidad',
      'ciudad',
      'nacionalidad',
      'telefono_1',
      'telefono_2',
      'estado_civil',
      'sexo',
      

    )
  dni = forms.CharField(max_length=15, validators=[validador])
  telefono_1 = forms.CharField(max_length=15, validators=[validador])
  telefono_2 = forms.CharField(max_length=15, validators=[validador])
  
    
class mesa_form(forms.ModelForm):   
  class Meta:
    model = MesaFinal
    fields = (
      'materia',
      'llamado'
    )
    
class edit_profile_form(forms.ModelForm):   
  class Meta:
    model = Usuario
    fields = (
      'username',
      'email',
      'nombre_completo',
      'fecha_nac',
      'dni',
      'direccion',
      'localidad',
      'ciudad',
      'nacionalidad',
      'telefono_1',
      'telefono_2',
      'estado_civil',
      'sexo',
      

    )

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = '__all__'

class ProfesorForm(forms.ModelForm):
    class Meta: 
        model = Profesor
        fields = '__all__' 

class PreceptorForm(forms.ModelForm):
    class Meta:
        model = Preceptor
        fields = '__all__'
class DirectivoForm(forms.ModelForm):
    class Meta:
        model = Directivo 
        fields = '__all__'


############################################################
class MateriaForm(forms.ModelForm):
      class Meta:
        model = Materia
        
        fields = ['nombre_materia', 'carrera', 'profesor', 'anio', 'Horario','inscripcionAbierta']
        widgets = {
           'nombre_materia': forms.TextInput(attrs={'class':'form-control'}),
           'carrera': forms.Select(attrs={'class':'form-control'}),
           'profesor': forms.Select(attrs={'class':'form-control'}),
           'anio': forms.Select(attrs={'class':'form-control'}),
           'dia': forms.Select(attrs={'class':'form-control'}),
           'Horario': forms.Select(attrs={'class':'form-control'}),
           'inscripcionAbierta': forms.CheckboxInput(attrs={'class':'form-check-input'})
        }
        labels = {
           'nombre_materia': 'Nombre materia',
           'carrera': 'Carrera',
           'profesor': 'Profesor',
           'anio': 'Año', 
           'dia' : 'Dia',
           'horario' : 'Horario',
           'inscripcionAbierta': 'Inscripción abierta',
        }


class MesaFinalForm(forms.ModelForm):
    class Meta:
        model = MesaFinal
        fields = ['materia', 'llamado','inscripcionAbierta']
        widgets = {
            'llamado': DateInput(attrs={'type': 'date'}),
            'inscripcionAbierta': forms.CheckboxInput(attrs={'class':'form-check-input'})
        }

class InscripcionFinalForm(forms.ModelForm):
    class Meta:
        model = InscripcionFinal
        fields = ['usuario', 'llamado']

class InscripcionMateriaForm(forms.ModelForm):
    class Meta:
        model = usuarios_materia
        fields = ['usuario', 'materia', 'modalidad']

class NotaFinalForm(forms.Form):
    nota_final = forms.DecimalField(max_digits=4, decimal_places=2, min_value=0, max_value=10)

class NotaCursadaForm(forms.ModelForm):
    class Meta:
        model = usuarios_materia
        fields = ('nota_cursada', 'nota_final')
        widgets = {
            'nota_cursada': forms.NumberInput(attrs={'min': '0', 'max': '10'}),
            'nota_final': forms.NumberInput(attrs={'min': '0', 'max': '10'}),
        }

    def clean_nota_cursada(self):
        nota = self.cleaned_data.get('nota_cursada')
        if nota is not None:
            if nota < 0 or nota > 10:
                raise forms.ValidationError("La nota debe estar entre 0 y 10.")
        return nota

    def clean_nota_final(self):
        nota = self.cleaned_data.get('nota_final')
        if nota is not None:
            if nota < 0 or nota > 10:
                raise forms.ValidationError("La nota debe estar entre 0 y 10.")
        return nota


class InscripcionFinalForm(forms.ModelForm):
    class Meta:
        model = InscripcionFinal
        fields = ['usuario', 'llamado', 'aprobada']

class FiltroInscripcionForm(forms.Form):
    estudiante = forms.CharField(required=False)
    materia = forms.CharField(required=False)
