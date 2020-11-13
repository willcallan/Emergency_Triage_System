import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PatientListComponent } from '../app/patient-list/patient-list.component';
import { StaffListComponent } from '../app/staff-list/staff-list.component';
import { AddPatientComponent } from '../app/add-patient/add-patient.component';
import { PatientDetailsComponent } from '../app/patient-details/patient-details.component';

const routes: Routes = [
  { path: 'patient-list', component: PatientListComponent },
  { path: 'staff-list', component: StaffListComponent },
  { path: 'add-patient', component: AddPatientComponent },
  { path: 'patient/:id', component: PatientDetailsComponent }
  ];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
