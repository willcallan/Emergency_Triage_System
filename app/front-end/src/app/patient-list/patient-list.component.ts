import { Component, OnInit } from '@angular/core';
import axios from 'axios';

import { Router } from '@angular/router';

import { BtnCellRenderer } from "../btn-cell-renderer.component";
import { NgxSpinnerService } from "ngx-spinner";

@Component({
  selector: 'app-patient-list',
  templateUrl: './patient-list.component.html',
  styleUrls: ['./patient-list.component.css']
})
export class PatientListComponent implements OnInit {

  constructor(private router: Router, private spinner: NgxSpinnerService) {  }

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
    {field: 'name'},
    {field: 'age'},
    {field: 'esi', headerName: 'ESI'},
    {field: 'code'},
    {field: 'display'},
    {field: 'location'},
    {field: 'checkedin', headerName: 'Checked-in'},
    {field: 'lastseen', headerName: 'Last Seen'},
    {field: 'seenby', headerName: 'Seen By'},
    {
      headerName: 'Details',
      cellRenderer: 'btnCellRenderer',
      cellRendererParams: {
        clicked: this.patientDetails.bind(this),
        label: 'Details',
        btnClass: 'btn btn-primary btn-sm'
      }
    }
  ];

  frameworkComponents = {
    btnCellRenderer: BtnCellRenderer
  };
  private gridApi;
  private gridColumnApi;

  patientDetails(patient){
    this.router.navigate(['/patient/'+patient.id]);
  }

  onGridReady(params) {
    this.gridApi = params.api;
    this.gridColumnApi = params.columnApi;
    const sortModel = [
      {colId: 'esi', sort: 'asc'}
    ];
    this.gridApi.setSortModel(sortModel);
    this.setAutoHeight();
  }

  setAutoHeight() {
    this.gridApi.setDomLayout('autoHeight');
  }

  rowData = [];

  rowClassRules = {
    'imm-warning': 'data.code == "ESI-1"',
    'emg-warning': 'data.code == "ESI-2"',
    'urg-warning': 'data.code == "ESI-3"',
    's-urg-warning': 'data.code == "ESI-4"',
    'no-urg-warning': 'data.code == "ESI-5"',
  };


  async ngOnInit(): Promise<void> {
    this.spinner.show();

    let staffUrl = this.baseUrl + 'practitioner';
    let staffList =(await axios.get(staffUrl)).data;
    let patientsUrl = this.baseUrl + 'patient';
    this.rowData = ((await axios.get(patientsUrl, this.config)).data);

    this.rowData.forEach(function(patient) {

      staffList.forEach(function(staff) {
        if(patient.seenby !== '' && patient.seenby == staff.id){
          patient.seenby = staff.name;
        }
      });
    });

    console.log(this.rowData);

    this.spinner.hide();
  }

}
