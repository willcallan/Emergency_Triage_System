import { Component, OnInit } from '@angular/core';
import axios from "axios";
import {BtnCellRenderer} from "../btn-cell-renderer.component";
import {Router} from "@angular/router";

@Component({
  selector: 'app-add-patient',
  templateUrl: './add-patient.component.html',
  styleUrls: ['./add-patient.component.css']
})
export class AddPatientComponent implements OnInit {


  baseUrl = 'http://127.0.0.1:5000/';
  config = {
    headers: {'Access-Control-Allow-Origin': '*'}
  };

  defaultColDef = {
    width: 150,
    flex: 1,
    wrapText: true,
    sortable: true,
    resizable: true,
    filter: true,
  };
  columnDefs = [
    {field: 'firstname', headerName: 'Firstname'},
    {field: 'lastname', headerName: 'Lastname'},
    {field: 'dob', headerName: 'Date of Birth'},
    {
      headerName: 'Add Patient',
      cellRenderer: 'btnCellRenderer',
      cellRendererParams: {
        clicked: this.addPatientFromSearch.bind(this),
        label: 'Add',
        btnClass: 'btn btn-primary btn-sm'
      }
    }
  ];
  rowData = [];

  enableSearch: any = false
  enableAdd: any = false;
  enableAddInjury: any = false;
  searchPatientId: any = '';
  searchFirstname: any = '';
  searchLastname: any = '';
  searchDOB: any = '';

  firstname: any = '';
  lastname: any = '';
  gender: any = '';
  dob: any = '';
  email: any = '';
  contactNumber: any = '';
  address: any = '';
  language: any = '';
  searchPatientList: any = '';

  private gridApi;
  private gridColumnApi;

  constructor(private router: Router) {  }

  ngOnInit(): void {
  }

  frameworkComponents = {
    btnCellRenderer: BtnCellRenderer
  };
  onGridReady(params) {
    this.gridApi = params.api;
    this.gridColumnApi = params.columnApi;
    const sortModel = [
      {colId: 'firstname', sort: 'asc'}
    ];
    this.gridApi.setSortModel(sortModel);
    this.setAutoHeight();
  }

  setAutoHeight() {
    this.gridApi.setDomLayout('autoHeight');
  }

  addPatientFromSearch(patient){
    console.log('add patient to our database')
    this.router.navigate(['/patient/'+patient.id]);
  }

  enableSearchPatient(){
    this.enableSearch = true;
    this.enableAdd = false;
    this.enableAddInjury = false;
  }

  enableAddPatient(){

    this.rowData = this.searchPatientList = [];
    this.enableSearch = false;
    this.enableAdd = true;
    this.enableAddInjury = false;
  }

  async searchPatient() {
    this.searchPatientList=[];
    if(this.searchPatientId != '')
    {
      console.log(this.searchPatientId);
      let patientIdUrl = this.baseUrl + 'patient?id=' + this.searchPatientId;
      console.log(patientIdUrl);
      this.searchPatientList = (await axios.get(patientIdUrl)).data;
    }

    let dob = '';

    if(this.searchDOB != '')
    {
      dob = this.formatDob(this.searchDOB);
    }

    let patientSearchUrl = this.baseUrl + 'patient/search?firstname=' + this.searchFirstname + '&lastname=' + this.searchLastname + '&dob='+dob;
    console.log(patientSearchUrl);

    this.searchPatientList = ((await axios.get(patientSearchUrl)).data);
    //let patientUrl = this.baseUrl + 'patient?id=' + 'bf3cb50a-d753-4ddc-ad83-839250edcba9';


    console.log(this.searchPatientList);
    this.rowData = this.searchPatientList;

  }

  async addPatient() {
    console.log(this.firstname + this.lastname + this.gender);

    let patientBody = {
      firstname: this.firstname,
      lastname: this.lastname,
      gender: this.gender,
      dob: this.formatDob(this.dob),
      email: this.email,
      contactNumber: this.contactNumber,
      address: this.address,
      language: this.language
    }

    console.log(patientBody);

    let patientAddUrl = this.baseUrl + 'patient/save';
    console.log(patientAddUrl);

    let addPatient = (await axios.post(patientAddUrl, patientBody)).data;
    console.log(addPatient);
    this.enableAddInjury = true;
    this.enableSearch = false;
    this.enableAdd = false;
  }

  formatDob(dob){
    let month = dob.getMonth() +1;
    let day = dob.getDate();
    if(month < 10)
      month = '0'+month;
    if(day < 10)
      day = '0'+day;
    return dob.getFullYear()+'-'+month+'-'+day;
  }
}
