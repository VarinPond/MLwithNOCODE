from . import views
from . import ml
from django.urls import path

urlpatterns = [
    path('', views.login_request, name="log_in"),
    path('register/', views.register_request, name="registry"),
    path('logout/', views.logout_request, name="log_out"),
    path('main/',  views.main, name="main"),
    path('main/delete/<int:table_id>',  views.delete_table, name="delete_table"),
    path('main/add/', views.add_table, name="add_table"),
    path('main/logout/', views.logout_request, name="main/log_out"),
    path('table/<int:table_id>', views.index, name="in_table"),
    path('table/<int:table_id>/<int:epoch>/<str:learning_rate>/<str:hd>',
         views.index, name="in_table"),
    path('table/<int:table_id>/add/', views.add, name="add"),
    path('table/<int:table_id>/delete/<int:id>', views.delete, name="delete"),
    path('table/<int:table_id>/deletehis/', ml.delete, name="deletehis"),
    path('table/<int:table_id>/train/', ml.train, name='train'),
    path('table/<int:table_id>/download/', ml.download_file, name='dowload'),
    path('table/<int:table_id>/predict/', ml.predict, name='predict'),
    path('table/<int:table_id>/edit/', views.edit, name='edit'),
    path('table/<int:table_id>/edit/submit_edit/',
         views.submit_edit, name='edit'),
]
