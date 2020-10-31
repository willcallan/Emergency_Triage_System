import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-add-patient',
  templateUrl: './add-patient.component.html',
  styleUrls: ['./add-patient.component.css']
})
export class AddPatientComponent implements OnInit {

  enableSearch: any = false
  enableAdd: any = false;
  enableAddInjury: any = false;
  inputPatient: any;

  firstname: any = '';
  lastname: any = '';
  gender: any = '';
  dob: any = '';
  email: any = '';
  contactNumber: any = '';
  address: any = '';
  language: any = '';

  constructor() { }

  ngOnInit(): void {
  }

  enableSearchPatient(){
    this.enableSearch = true;
    this.enableAdd = false;
    this.enableAddInjury = false;
  }

  enableAddPatient(){
    this.enableSearch = false;
    this.enableAdd = true;
    this.enableAddInjury = false;
  }

  searchPatient(){
    console.log(this.inputPatient);
  }

  addPatient(){
    console.log(this.firstname + this.lastname + this.gender);
    //add patient to fhir

    this.enableAddInjury = true;
    this.enableSearch = false;
    this.enableAdd = false;
  }

  addInjury(){
    console.log(this.inputPatient);
  }
}
