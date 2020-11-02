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
  baseUrl = 'http://172.20.160.1:5000/';

  async ngOnInit(): Promise<void> {
    this.patientId = this.route.snapshot.paramMap.get('id');

    //let patientUrl = this.baseUrl + 'patient?id=' + id;
    let patientUrl = this.baseUrl + 'patient?id=' + 'bf3cb50a-d753-4ddc-ad83-839250edcba9';
    this.patient = (await axios.get(patientUrl)).data;

    console.log(this.patient);
  }

}
