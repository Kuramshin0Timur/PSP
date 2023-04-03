package com.example.sigmamessage

import com.google.gson.Gson
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.logging.HttpLoggingInterceptor

data class SignInRequestBody (
    val login: String,
    val id: Int
)

val contentType = "application/json; charset=utf-8".toMediaType()


fun main() {
    val loggingInterceptor = HttpLoggingInterceptor()
        .setLevel(HttpLoggingInterceptor.Level.BODY)

    val gson = Gson()

    val client = OkHttpClient.Builder()
        .addInterceptor(loggingInterceptor)
        .build()

    val requestBody = SignInRequestBody(
        login = "fuck",
        id = 19
    )

    val requestBodyString = gson.toJson(requestBody)
    val body = requestBodyString.toRequestBody(contentType)


    val request = Request.Builder()
        .delete()
        .url("http://127.0.0.1:3000/api/users/2")
        .build()

    val call = client.newCall(request)
    val response = call.execute()
    if (response.isSuccessful) {
    //    val responseBodyString = response.body!!.string()
       println("responseBodyString")
    } else {
        throw java.lang.IllegalStateException("Ooops")
    }
}