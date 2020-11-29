import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';

export interface DialogData {
  bodyPart: string;
  type: string;
  painLevel: number;
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
  systems: any;
  bloodClasses: any;
  eyeResponses: any;
  verbalResponses: any;
  motorResponses: any;

  enableArea: any = true;
  enableSystem: any = false;

  ngOnInit(): void {
    this.data= {
      bodyPart: '',
      type:'',
      painLevel:0,
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

    this.systems = [
      {value: 'bloodLoss', viewValue: 'Blood Loss'},
      {value: 'GCS', viewValue: 'Glasgow Coma Scale'},
      {value: 'smokeInhalation', viewValue: 'Smoke Inhalation'}
    ];

    this.bloodClasses = [
      {value: 'Class 1', viewValue: 'Class 1: <750 mL or <15% blood volume'},
      {value: 'Class 2', viewValue: 'Class 2: 750-1500 mL or 15-30% blood volume'},
      {value: 'Class 3', viewValue: 'Class 3: 1500-2000 mL or 30-40% blood volume'},
      {value: 'Class 4', viewValue: 'Class 4: >2000 mL or >40% blood volume'}
    ];

    this.eyeResponses = [
      {value: '1', viewValue: 'Spontaneous - open with blinking at baseline'},
      {value: '2', viewValue: 'To verbal stimuli, command, speech'},
      {value: '3', viewValue: 'To pain only (not applied to face)'},
      {value: '4', viewValue: 'No response'}
    ];

    this.verbalResponses = [
      {value: '1', viewValue: 'Oriented'},
      {value: '2', viewValue: 'Confused conversation, but able to answer questions'},
      {value: '3', viewValue: 'Inappropriate words'},
      {value: '4', viewValue: 'Incomprehensible speech'},
      {value: '5', viewValue: 'No response'}
    ];

    this.motorResponses = [
      {value: '1', viewValue: 'Obeys commands for movement'},
      {value: '2', viewValue: 'Purposeful movement to painful stimulus'},
      {value: '3', viewValue: 'Withdraws in response to pain'},
      {value: '4', viewValue: 'Flexion in response to pain (decorticate posturing)'},
      {value: '5', viewValue: 'Extension response in response to pain (decerebrate posturing)'},
      {value: '6', viewValue: 'No response'}
    ];

  }

  addInjury(){
    console.log('add');
  }

  selectionChange(){
    console.log('changed selection');
    this.data.bloodLoss = '';
    this.data.eyeResponse = '';
    this.data.verbalResponse = '';
    this.data.motorResponse = '';
  }

  updateView(type){

    console.log(type);
    this.data.system = '';

    console.log('enableArea', this.enableArea);
    console.log('enableSystem', this.enableSystem);

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

    console.log('enableArea', this.enableArea);
    console.log('enableSystem', this.enableSystem);
/*
    if(this.enableSystem)
    {
      this.data.typeOfInjury = 'system';
    }
    else if(this.enableArea)
    {
      this.data.typeOfInjury = 'area';
    }*/

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
