import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';

export interface DialogData {
  bodyPart: string;
  type: string;
  painLevel: string;
  notes: string;
  diagnosis: string;
  severity: string;

  bloodLoss: string;
  system: string;
  eyeResponse: string;

  verbalResponse: string;
  motorResponse: string;

  typeOfInjury: string;
}


@Component({
  selector: 'app-add-injury',
  templateUrl: './add-injury.component.html',
  styleUrls: ['./add-injury.component.css']
})
export class AddInjuryComponent implements OnInit {

  constructor(@Inject(MAT_DIALOG_DATA) public data: DialogData) { }

  types: any;
  bodyParts: any;
  enableArea: any = true;
  enableSystem: any = false;

  ngOnInit(): void {
    this.data= {
      bodyPart: '',
      type:'',
      painLevel:'',
      notes:'',
      diagnosis:'',
      severity:'',
      bloodLoss:'',
      system:'',
      eyeResponse:'',
      verbalResponse:'',
      motorResponse:'',
      typeOfInjury: 'area'
    };

    this.bodyParts = [
      {value: 'face', viewValue: 'Face'},
      {value: 'scalp', viewValue: 'Scalp'},
      {value: 'frontOfNeck', viewValue: 'Anterior Portion of Neck'},
      {value: 'backOfNeck', viewValue: 'Posterior Portion of Neck'},
      {value: 'leftShoulder', viewValue: 'Left Shoulder'},
      {value: 'rightShoulder', viewValue: 'Right Shoulder'},
      {value: 'leftUpperArm', viewValue: 'Left Upper Arm'},
      {value: 'rightUpperArm', viewValue: 'Right Upper Arm'},
      {value: 'leftLowerArm', viewValue: 'Left Forearm'},
      {value: 'rightLowerArm', viewValue: 'Right Forearm'},
      {value: 'leftHand', viewValue: 'Left Hand'},
      {value: 'rightHand', viewValue: 'Right Hand'},
      {value: 'chest', viewValue: 'Chest'},
      {value: 'abdomen', viewValue: 'Abdomen'},
      {value: 'back', viewValue: 'Back'},
      {value: 'groin', viewValue: 'Groin'},
      {value: 'buttock', viewValue: 'Buttock'},
      {value: 'leftUpperLeg', viewValue: 'Left Thigh'},
      {value: 'rightUpperLeg', viewValue: 'Right Thigh'},
      {value: 'leftLowerLeg', viewValue: 'Left Lower Leg'},
      {value: 'rightLowerLeg', viewValue: 'Right Lower Leg'},
      {value: 'leftFoot', viewValue: 'Left Foot'},
      {value: 'rightFoot', viewValue: 'Right Foot'}
    ];

   this.types = [
     {value: 'abrasion', viewValue: 'Abrasion'},
     {value: 'avulsion', viewValue: 'Avulsion'},
     {value: 'bite', viewValue: 'Bite'},
     {value: 'blister', viewValue: 'Blister'},
     {value: 'burn', viewValue: 'Burn'},
     {value: 'gunshotWound', viewValue: 'Gunshot Wound'},
     {value: 'contusion', viewValue: 'Contusion'},
     {value: 'crushInjury', viewValue: 'Crush Injury'},
     {value: 'erythema', viewValue: 'Erythema'},
     {value: 'fissure', viewValue: 'Fissure'},
     {value: 'laceration', viewValue: 'Laceration'},
     {value: 'maceration', viewValue: 'Maceration'},
     {value: 'pressureUlcer', viewValue: 'Pressure Ulcer'},
     {value: 'ulcer', viewValue: 'Ulcer'},
     {value: 'puncture', viewValue: 'Puncture'},
     {value: 'rash', viewValue: 'Rash'},
     {value: 'graft', viewValue: 'Graft'},
     {value: 'surgicalIncision', viewValue: 'Surgical Incision'},
     {value: 'trauma', viewValue: 'Trauma'}
    ];
  }





  addInjury(){
    console.log('add');
  }

  updateView(type){

    console.log(type);

    if(type == 'system' && this.enableSystem)
    {
      this.enableArea = true;
    }

    if(type == 'system' && !this.enableSystem)
    {
      this.enableArea = false;
    }

    if(type == 'area' && this.enableArea)
    {
      this.enableSystem = true;
    }

    if(type == 'area' && !this.enableArea)
    {
      this.enableSystem = false;
    }

    if(this.enableSystem)
    {
      this.data.typeOfInjury = 'system';
    }
    else if(this.enableArea)
    {
      this.data.typeOfInjury = 'area';
    }

    /*

    if(type == 'area')
    {

      console.log("areaa");
      this.enableArea = true;
      this.enableSystem = false;
      this.data.typeOfInjury = 'area';
    }
    console.log('add');*/
  }

}
