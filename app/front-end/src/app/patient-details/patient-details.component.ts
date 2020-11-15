import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import axios from "axios";

@Component({
  selector: 'app-patient-details',
  templateUrl: './patient-details.component.html',
  styleUrls: ['./patient-details.component.css']
})
export class PatientDetailsComponent implements OnInit {

  constructor(private route: ActivatedRoute) { }

  patientId:any;
  patient: any
  baseUrl = 'http://127.0.0.1:5000/';
  backgroundColor = '';

  async ngOnInit(): Promise<void> {
    this.patientId = this.route.snapshot.paramMap.get('id');

    let patientUrl = this.baseUrl + 'patient?id=' + this.patientId;
    //let patientUrl = this.baseUrl + 'patient?id=' + 'bf3cb50a-d753-4ddc-ad83-839250edcba9';
    this.patient = (await axios.get(patientUrl)).data;

    this.setBg();

    console.log(this.patient);
  }

  update(){
    console.log('update patient');
    this.setBg();
  }

  addVisit(){
    console.log('add visit');
  }
  addInjury(){
    console.log('add injury');
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
