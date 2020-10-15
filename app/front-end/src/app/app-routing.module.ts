import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PatientListComponent } from '../app/patient-list/patient-list.component';
import { StaffListComponent } from '../app/staff-list/staff-list.component';
import { AddPatientComponent } from '../app/add-patient/add-patient.component';

const routes: Routes = [
  { path: 'patient-list', component: PatientListComponent },
  { path: 'staff-list', component: StaffListComponent },
  { path: 'add-patient', component: AddPatientComponent }
  ];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
