import { FormGroup, Validators, FormGroupName } from '@angular/forms';

export class FormValidator {

    isTouched(form: FormGroup, controlName: string): boolean {
        return form.get(controlName).touched;
    }

    isRequired(form: FormGroup, controlName: string): boolean {
        return form.get(controlName)?.errors?.required;
    }

}