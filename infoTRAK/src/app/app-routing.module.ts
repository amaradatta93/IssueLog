import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AuthComponent } from './auth/auth.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { AddIssueComponent } from './add-issue/add-issue.component';
import { ModifyIssueComponent } from './modify-issue/modify-issue.component';

import { AuthGuard } from './_helpers/auth.guard';


const routes: Routes = [
  {path: '', component: DashboardComponent, canActivate: [AuthGuard]},
  {path: 'auth', component: AuthComponent},
  {path: 'add-issue', component: AddIssueComponent, canActivate: [AuthGuard]},
  {path: 'modify-issue/:id', component: ModifyIssueComponent, canActivate: [AuthGuard]}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
