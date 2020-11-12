import { Component, OnDestroy } from "@angular/core";

import { ICellRendererAngularComp } from "@ag-grid-community/angular";

@Component({
  selector: "btn-cell-renderer",
  template: `
    <button mat-raised-button (click)="btnClickedHandler()">Details</button>
  `
})
export class BtnCellRenderer implements ICellRendererAngularComp, OnDestroy {
  private params: any;

  agInit(params: any): void {
    this.params = params;
  }

  btnClickedHandler() {
    this.params.clicked(this.params.data);
  }

  ngOnDestroy() {
  }

  refresh(params: any): boolean {
    return false;
  }
}
