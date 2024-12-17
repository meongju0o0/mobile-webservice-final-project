package com.example.androidclassroommanager;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Header;

public interface ClassroomPhotoApi {
    @GET("api/classroom_photos/")
    Call<List<ClassroomPhoto>> getClassroomPhotos(@Header("Authorization") String token);
}