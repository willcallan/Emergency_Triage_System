import { Component, OnInit } from '@angular/core';
import axios from 'axios';

import { Router } from '@angular/router';

import { BtnCellRenderer } from "../btn-cell-renderer.component";

@Component({
  selector: 'app-patient-list',
  templateUrl: './patient-list.component.html',
  styleUrls: ['./patient-list.component.css']
})
export class PatientListComponent implements OnInit {

  constructor(private router: Router) {  }

  baseUrl = 'http://172.20.160.1:5000/';
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
    {field: 'status'},
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
    console.log(patient);
    this.router.navigate(['/patient/'+patient.age]);
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
  /*rowData = [
    {
      name: 'Giacomo Guilizzoni',
      age: '30',
      esi: '1',
      code: 'imm',
      display: 'Immediate',
      location: 'ICU',
      status: '1',
      checkedin: '9 Hours ago',
      lastseen: '2 mins',
      seenby: 'Doctor'
    },
    {
      name: 'Giacomo Guilizzoni',
      age: '40',
      esi: '2',
      code: 'emg',
      display: 'Emergency',
      location: 'ICU',
      status: '1',
      checkedin: '9 Hours ago',
      lastseen: '2 mins',
      seenby: 'Doctor'
    },
    {
      name: 'Giacomo Guilizzoni',
      age: '46',
      esi: '3',
      code: 'urg',
      display: 'Urgent',
      location: 'ICU',
      status: '1',
      checkedin: '9 Hours ago',
      lastseen: '2 mins',
      seenby: 'Doctor'
    },
    {
      name: 'Giacomo Guilizzoni',
      age: '43',
      esi: '4',
      code: 's-urg',
      display: 'Semi Urgent',
      location: 'ICU',
      status: '1',
      checkedin: '9 Hours ago',
      lastseen: '2 mins',
      seenby: 'Doctor'
    },
    {
      name: 'Giacomo Guilizzoni',
      age: '76',
      esi: '5',
      code: 'no-urg',
      display: 'Non Urgent',
      location: 'ICU',
      status: '1',
      checkedin: '9 Hours ago',
      lastseen: '2 mins',
      seenby: 'Doctor'
    },
    {
      name: 'Giacomo Guilizzoni',
      age: '23',
      esi: '1',
      code: 'imm',
      display: 'Immediate',
      location: 'ICU',
      status: '1',
      checkedin: '9 Hours ago',
      lastseen: '2 mins',
      seenby: 'Doctor'
    },
    {
      name: 'Giacomo Guilizzoni',
      age: '65',
      esi: '3',
      code: 'urg',
      display: 'Urgent',
      location: 'ICU',
      status: '1',
      checkedin: '9 Hours ago',
      lastseen: '2 mins',
      seenby: 'Doctor'
    },
    {
      name: 'Giacomo Guilizzoni',
      age: '02',
      esi: '4',
      code: 's-urg',
      display: 'Semi Urgent',
      location: 'ICU',
      status: '1',
      checkedin: '9 Hours ago',
      lastseen: '2 mins',
      seenby: 'Doctor'
    },
    {
      name: 'Giacomo Guilizzoni',
      age: '08',
      esi: '2',
      code: 'emg',
      display: 'Emergency',
      location: 'ICU',
      status: '1',
      checkedin: '9 Hours ago',
      lastseen: '2 mins',
      seenby: 'Doctor'
    },
    {
      name: 'Giacomo Guilizzoni',
      age: '41',
      esi: '3',
      code: 'urg',
      display: 'Urgent',
      location: 'ICU',
      status: '1',
      checkedin: '9 Hours ago',
      lastseen: '2 mins',
      seenby: 'Doctor'
    },
    {
      name: 'Giacomo Guilizzoni',
      age: '49',
      esi: '4',
      code: 's-urg',
      display: 'Semi Urgent',
      location: 'ICU',
      status: '1',
      checkedin: '9 Hours ago',
      lastseen: '2 mins',
      seenby: 'Doctor'
    }

  ];*/

  rowClassRules = {
    'imm-warning': 'data.code == "ESI-1"',
    'emg-warning': 'data.code == "ESI-2"',
    'urg-warning': 'data.code == "ESI-3"',
    's-urg-warning': 'data.code == "ESI-4"',
    'no-urg-warning': 'data.code == "ESI-5"',
  };


  async ngOnInit(): Promise<void> {
    let patientsUrl = this.baseUrl + 'patient';
    this.rowData = (await axios.get(patientsUrl, this.config)).data;
    console.log(this.rowData);
  }

}
