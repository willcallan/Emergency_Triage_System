import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import axios from 'axios';
import {AddInjuryComponent} from "../add-injury/add-injury.component";
import {AddVisitComponent} from "../add-visit/add-visit.component";
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-patient-details',
  templateUrl: './patient-details.component.html',
  styleUrls: ['./patient-details.component.css']
})
export class PatientDetailsComponent implements OnInit {

  constructor(public dialog: MatDialog, private route: ActivatedRoute) { }

  patientId:any;
  patient: any
  notes: any
  history: any
  emergencyContacts: any
  observation: any
  baseUrl = 'http://127.0.0.1:5000/';
  backgroundColor = '';
  newLocation = '';
  systemInjuries: any=[];
  bodyInjuries: any=[];
  staffList: any=[];
  staff:any;
  patientData:any;
  address:any = '';


  defaultColDef = {
    width: 150,
    flex: 1,
    wrapText: true,
    sortable: true,
    resizable: true,
    filter: true,
  };
  systemColumnDefs = [
    {field: 'system', headerName: 'System'},
    {field: 'time'},
    {field: 'value'}
  ];

  bodyColumnDefs = [
    {field: 'bodyPart', headerName: 'Body Part'},
    {field: 'time'},
    {field: 'injury'},
    {field: 'severity'}
  ];
  private gridApi;
  private gridColumnApi;

  onGridReady(params) {
    this.gridApi = params.api;
    this.gridColumnApi = params.columnApi;
    const sortModel = [
      {colId: 'time', sort: 'asc'}
    ];
    this.gridApi.setSortModel(sortModel);
    this.setAutoHeight();
  }

  setAutoHeight() {
    this.gridApi.setDomLayout('autoHeight');
  }

  async ngOnInit(): Promise<void> {
    this.patientId = this.route.snapshot.paramMap.get('id');

    let patientUrl = this.baseUrl + 'patient?id=' + this.patientId;
    this.patientData = (await axios.get(patientUrl)).data;
    let staffUrl = this.baseUrl + 'practitioner';
    this.staffList =(await axios.get(staffUrl)).data;

    console.log('patientData',this.patientData);
    this.patient = this.patientData.patient;
    this.notes = this.patientData.notes;
    this.history = this.patientData.history;
    this.emergencyContacts = this.patientData.emergencyContacts;

    let practitioners = this.staffList;

    this.notes.forEach(function(note) {

      practitioners.forEach(function(staff) {
        if(note.author == staff.id){
          note.name = staff.name;
        }
      });
    });

    if(this.patient.address)
    {
      this.address = this.patient.address.street +', '+this.patient.address.city +', '+this.patient.address.state;
    }

    this.staff = this.patient.seenby;

    this.setBg();

    await this.updateInjuryTable();

    console.log(this.patient);
    console.log(this.observation);
    console.log(this.systemInjuries);
    console.log(this.bodyInjuries);
  }

  async updateInjuryTable()
  {
    console.log('update injury table');
    let observationUrl = this.baseUrl + 'observations?id=' + this.patientId;
    this.observation = (await axios.get(observationUrl)).data;

    let sysInjuries = [];
    let bdyInjuries = [];

    if(this.observation.length > 0)
    {
      this.observation.forEach(function(obsr) {
        if(obsr.system){
          sysInjuries.push(obsr);
        }
        else
        {
          bdyInjuries.push(obsr);
        }
      });
    }

    this.systemInjuries = sysInjuries;
    this.bodyInjuries = bdyInjuries;
  }

  async update() {

    let updateBody = {id: this.patientId, code: this.patient.code, location: null, seenby: null};

    this.patientData.patient.code = this.patient.code;
    this.patientData.patient.esi = this.patient.code.charAt(4);

    if (this.newLocation !== this.patient.location && this.newLocation !== '') {

      this.patientData.patient.location = this.newLocation;
    }

    if (this.patient.seenby != undefined) {
      this.patientData.patient.seenby = this.staff;
    }

    console.log(this.patientData);


    let patientUpdateUrl = this.baseUrl + 'patient/save';
    let resource = (await axios.post(patientUpdateUrl, this.patientData)).data;

    console.log(resource);
    this.setBg();
  }

  addVisit(){
    console.log('add visit');
    const dialogRef = this.dialog.open(AddVisitComponent, {
      width: '700px',
      data: {patientId:this.patientId}
    });

    dialogRef.afterClosed().subscribe(async result => {

      if(result)
      {
        console.log('Dialog result: ', result);
        let visitBody = {
          note: result,
          time : new Date(),
          author: this.patient.seenby
        }

        this.patientData.notes.push(visitBody);

        console.log(this.patientData);


        let patientUpdateUrl = this.baseUrl + 'patient/save';
        let resource = (await axios.post(patientUpdateUrl, this.patientData)).data;

        console.log(resource);

        await this.ngOnInit();

      }

    });
  }

  addInjury(){
    console.log('add injury');
    const dialogRef = this.dialog.open(AddInjuryComponent, {
      width: '730px',
      data: {patientId:this.patientId}
    });

    dialogRef.afterClosed().subscribe(async result => {

      if(result)
      {
        console.log('Dialog result: ', result);

        let observationUrl = this.baseUrl + 'observation/save';

        let postBody = {};

        if(result.system == ''){
          postBody = this.getBodyAreaInjuryBody(result)
        }
        else {
          postBody = this.getSystemInjuryBody(result)
        }

        console.log(postBody);
        let resource = (await axios.post(observationUrl, postBody)).data;

        console.log(resource);
        setTimeout("", 3000);
        await this.updateInjuryTable();
      }

    });
  }

  getBodyAreaInjuryBody(result){
    let body = {
      patientID: this.patientId,
      bodyPart: result.bodyPart,
      injury: result.type,
      severity: result.painLevel,
      notes: result.notes
    }
    return body;
  }


  getSystemInjuryBody(result){
    let body = {};

    if(result.system == 'bloodLoss')
    {
      body = {
        patientID: this.patientId,
        notes: result.notes,
        system: 'bloodLoss',
        value: result.bloodLoss
      }
    }
    else if(result.system == 'GCS')
    {
      body = {
        patientID: this.patientId,
        notes: result.notes,
        system: 'GCS',
        value: {
          eye: result.eyeResponse,
          verbal: result.verbalResponse,
          motor: result.motorResponse,
        }
      }
    }
    else if(result.system == 'smokeInhalation')
    {
      body = {
        patientID: this.patientId,
        notes: result.notes,
        system: 'smokeInhalation'
      }
    }

    return body;
  }

  setBg(){
    if(this.patient.code == "ESI-1")
    {
      this.backgroundColor= "imm-warning"
    }
    else if(this.patient.code == "ESI-2")
    {
      this.backgroundColor  = "emg-warning"
    }
    else if(this.patient.code == "ESI-3")
    {
      this.backgroundColor= "urg-warning"
    }
    else if(this.patient.code == "ESI-4")
    {
      this.backgroundColor  = "s-urg-warning"
    }
    else if(this.patient.code == "ESI-5")
    {
      this.backgroundColor  = "no-urg-warning"
    }
  }
}
