package com.example.androidclassroommanager;

import retrofit2.http.Body;
import retrofit2.http.POST;
import retrofit2.Call;

public interface AuthApi {
    @POST("api/login/")
    Call<LoginResponse> login(@Body LoginRequest loginRequest);
}