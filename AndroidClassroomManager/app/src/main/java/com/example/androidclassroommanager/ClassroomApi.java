package com.example.androidclassroommanager;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.GET;

public interface ClassroomApi {
    @GET("api/classrooms/")  // Django 서버의 엔드포인트 URL
    Call<List<Classroom>> getClassrooms();
}
