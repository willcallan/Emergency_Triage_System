import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-staff-list',
  templateUrl: './staff-list.component.html',
  styleUrls: ['./staff-list.component.css']
})
export class StaffListComponent implements OnInit {

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
    {field: 'professionType', headerName: 'Profession Type'},
    {field: 'name'},
    {field: 'speciality'},
    {field: 'email'},
    {field: 'contact'}
  ];
  private gridApi;
  private gridColumnApi;

  onGridReady(params) {
    this.gridApi = params.api;
    this.gridColumnApi = params.columnApi;
    const sortModel = [
      {colId: 'professionType', sort: 'asc'}
    ];
    this.gridApi.setSortModel(sortModel);
    this.setAutoHeight();
  }

  setAutoHeight() {
    this.gridApi.setDomLayout('autoHeight');
  }

  rowData = [
    { professionType: 'Doctor', name: 'Liz', speciality: 'Cardiologist', email: 'abc@xyz.com', contact: '000.000.0000' },
    { professionType: 'Nurse', name: 'Jack', speciality: 'Internal', email: 'abc@xyz.com', contact: '000.000.0000' },
    { professionType: 'Nurse', name: 'Patel', speciality: 'Cardiologist', email: 'abc@xyz.com', contact: '000.000.0000' },
    { professionType: 'Doctor', name: 'Liz', speciality: 'Cardiologist', email: 'abc@xyz.com', contact: '000.000.0000' },
    { professionType: 'Doctor', name: 'Liz', speciality: 'Cardiologist', email: 'abc@xyz.com', contact: '000.000.0000' },
    { professionType: 'Doctor', name: 'Liz', speciality: 'Cardiologist', email: 'abc@xyz.com', contact: '000.000.0000' },
    { professionType: 'Doctor', name: 'Liz', speciality: 'Cardiologist', email: 'abc@xyz.com', contact: '000.000.0000' },
    { professionType: 'Doctor', name: 'Liz', speciality: 'Cardiologist', email: 'abc@xyz.com', contact: '000.000.0000' },
    { professionType: 'Doctor', name: 'Liz', speciality: 'Cardiologist', email: 'abc@xyz.com', contact: '000.000.0000' }
  ]

  ngOnInit(): void {
  }

}
