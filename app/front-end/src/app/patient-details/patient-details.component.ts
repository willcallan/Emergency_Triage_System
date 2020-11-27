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

  async ngOnInit(): Promise<void> {
    this.patientId = this.route.snapshot.paramMap.get('id');

    let patientUrl = this.baseUrl + 'patient?id=' + this.patientId;
    //let patientUrl = this.baseUrl + 'patient?id=' + 'bf3cb50a-d753-4ddc-ad83-839250edcba9';
    let patientData = (await axios.get(patientUrl)).data;
    this.patient = patientData.patient;
    this.notes = patientData.notes;
    this.history = patientData.history;
    this.emergencyContacts = patientData.emergencyContacts;

    this.setBg();

    console.log(this.patient);
  }

  update(){
    console.log('update patient');
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
          notes: result,
          timeStamp : new Date(),
          practitioner: '1221'
        }

        console.log(visitBody);

        //let visitUrl = this.baseUrl + 'observation/save';
        //let resource = (await axios.post(visitUrl, visitBody)).data;

        //console.log(resource);

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

        let postBody = this.getInjuryBody(result);

        console.log(postBody);
        let resource = (await axios.post(observationUrl, postBody)).data;

        console.log(resource);
      }

    });
  }

  getInjuryBody(result){
    let body = {
      patientID: this.patientId,
      bodyPart: result.bodyPart,
      injury: result.type
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
