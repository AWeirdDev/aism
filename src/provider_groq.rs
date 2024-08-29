use anyhow::Error;
use reqwest::Client;
use serde_json::json;

use crate::provider_base::{Message, Provider};

#[derive(Clone)]
pub struct Groq {
    api_key: String,
}

impl Provider for Groq {
    fn new(api_key: String) -> Self {
        Self { api_key }
    }

    async fn inquire(&self, messages: Vec<Message>) -> Result<Message, Error> {
        let client = Client::new();
        let res = client
            .post("https://api.groq.com/openai/v1/chat/completions")
            .header("Content-Type", "application/json")
            .header("Authorization", format!("Bearer {}", self.api_key))
            .json(&json!({
                "model": "llama3-8b-8192",
                "messages": messages
            }))
            .send()
            .await?
            .error_for_status()?;

        let result: serde_json::Value = res.json().await?;
        let message: Message = serde_json::from_value(result["choices"][0]["message"].to_owned())?;

        Ok(message)
    }
}
