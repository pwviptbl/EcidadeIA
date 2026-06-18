<?php

use App\Http\Controllers\AgentController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');

Route::get('/sessions', [AgentController::class, 'sessions']);
Route::post('/ask', [AgentController::class, 'ask']);
Route::get('/history/{session_id}', [AgentController::class, 'history']);
Route::delete('/history/{session_id}', [AgentController::class, 'clear']);
