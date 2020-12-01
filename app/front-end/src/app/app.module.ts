import { BrowserModule } from '@angular/platform-browser';

import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { PatientListComponent } from './patient-list/patient-list.component';
import { StaffListComponent } from './staff-list/staff-list.component';
import { AddPatientComponent } from './add-patient/add-patient.component';
import { AgGridModule } from 'ag-grid-angular';
import {MatButtonModule} from '@angular/material/button';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {FormsModule} from '@angular/forms';
import {MatInputModule} from '@angular/material/input';
import {MatDatepickerModule} from '@angular/material/datepicker';
import {MatNativeDateModule, MatRippleModule} from '@angular/material/core';
import {MatAutocompleteModule} from '@angular/material/autocomplete';
import {MatSelectModule} from "@angular/material/select";
import {MatIconModule} from '@angular/material/icon';
import { MatDialogModule } from '@angular/material/dialog';
import { PatientDetailsComponent } from './patient-details/patient-details.component';
import { BtnCellRenderer } from './btn-cell-renderer.component';
import { CommonModule } from '@angular/common';
import { AddInjuryComponent } from './add-injury/add-injury.component';
import { AddVisitComponent } from './add-visit/add-visit.component';

import {MatDividerModule} from '@angular/material/divider';
import {MatSliderModule} from '@angular/material/slider';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';
import { NgxSpinnerModule } from "ngx-spinner";

@NgModule({
  declarations: [
    AppComponent,
    PatientListComponent,
    StaffListComponent,
    AddPatientComponent,
    PatientDetailsComponent,
    BtnCellRenderer,
    AddInjuryComponent,
    AddVisitComponent
  ],
  imports: [
    BrowserModule,
    AgGridModule.withComponents([BtnCellRenderer]),
    MatButtonModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    NgxSpinnerModule,
    MatInputModule,
    MatDividerModule,
    MatSliderModule,
    MatSlideToggleModule,
    MatDatepickerModule,
    MatDialogModule,
    MatNativeDateModule,
    MatRippleModule,
    MatAutocompleteModule,
    MatSelectModule,
    MatIconModule,
    FormsModule,
    CommonModule
  ],
  providers: [],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  bootstrap: [AppComponent]
})
export class AppModule { }
