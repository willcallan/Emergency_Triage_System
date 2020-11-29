import { Component, OnInit } from '@angular/core';
import axios from 'axios';

@Component({
  selector: 'app-staff-list',
  templateUrl: './staff-list.component.html',
  styleUrls: ['./staff-list.component.css']
})
export class StaffListComponent implements OnInit {


  baseUrl = 'http://127.0.0.1:5000/';
  config = {
    headers: {'Access-Control-Allow-Origin': '*'}
  };
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
    {field: 'specialty'},
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
  rowData=[];

  async ngOnInit(): Promise<void> {

    let staffUrl = this.baseUrl + 'staff';
    this.rowData = (await axios.get(staffUrl, this.config)).data;
    console.log(this.rowData);
  }

}
