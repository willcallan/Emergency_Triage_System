import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-patient-list',
  templateUrl: './patient-list.component.html',
  styleUrls: ['./patient-list.component.css']
})
export class PatientListComponent implements OnInit {

  constructor() {
  }

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
    {field: 'seenby', headerName: 'Seen By'}
  ];
  private gridApi;
  private gridColumnApi;

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

  rowData = [
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

  ];

  rowClassRules = {
    'imm-warning': 'data.code == "imm"',
    'emg-warning': 'data.code == "emg"',
    'urg-warning': 'data.code == "urg"',
    's-urg-warning': 'data.code == "s-urg"',
    'no-urg-warning': 'data.code == "no-urg"',
  };


  ngOnInit(): void {
  }

}
