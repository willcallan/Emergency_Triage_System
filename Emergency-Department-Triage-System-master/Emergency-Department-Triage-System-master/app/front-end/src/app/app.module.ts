import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { PatientListComponent } from './patient-list/patient-list.component';
import { StaffListComponent } from './staff-list/staff-list.component';
import { AddPatientComponent } from './add-patient/add-patient.component';
import { AgGridModule } from 'ag-grid-angular';
@NgModule({
  declarations: [
    AppComponent,
    PatientListComponent,
    StaffListComponent,
    AddPatientComponent
  ],
  imports: [
    BrowserModule,
    AgGridModule.withComponents([]),
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
