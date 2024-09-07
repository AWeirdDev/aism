use anyhow::Error;

pub enum Role {
    System,
    User,
    Assistant,
}

impl Role {
    pub fn to_string(&self) -> String {
        match self {
            Self::System => "system",
            Self::User => "user",
            Self::Assistant => "assistant",
        }
        .to_string()
    }

    pub fn from_name(name: String) -> Option<Self> {
        match name.as_str() {
            "system" => Some(Self::System),
            "user" => Some(Self::User),
            "assistant" => Some(Self::Assistant),
            _ => None,
        }
    }
}

impl serde::Serialize for Role {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        serializer.serialize_str(&self.to_string())
    }
}

impl<'de> serde::Deserialize<'de> for Role {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: serde::Deserializer<'de>,
    {
        let s = String::deserialize(deserializer)?;
        match s.as_str() {
            "system" => Ok(Self::System),
            "user" => Ok(Self::User),
            "assistant" => Ok(Self::Assistant),
            _ => Err(serde::de::Error::custom("invalid role")),
        }
    }
}

#[derive(serde::Serialize, serde::Deserialize)]
pub struct Message {
    pub role: Role,
    pub content: String,
}

pub trait Provider {
    fn new(api_key: String) -> Self;
    async fn inquire(&self, messages: Vec<Message>) -> Result<Message, Error>;
}
