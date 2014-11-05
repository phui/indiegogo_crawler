CREATE TABLE igg_user_profile(
    uid INT NOT NULL,
    url VARCHAR(70) NOT NULL,
    name VARCHAR(50) NOT NULL,
    location VARCHAR(50) NOT NULL,
    num_campaigns INT NOT NULL,
    num_contrib INT NOT NULL,
    num_referrals INT NOT NULL,
    num_comments INT NOT NULL,
    insert_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE igg_user_verify(
    uid INT NOT NULL,
    verify VARCHAR(70) NOT NULL,
    insert_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE igg_user_campaign(
    uid INT NOT NULL,
    pid INT NOT NULL,
    insert_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE igg_user_contribution(
    uid INT NOT NULL,
    pid INT NOT NULL,
    insert_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE igg_user_following(
    uid INT NOT NULL,
    pid INT NOT NULL,
    insert_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE igg_user_comment(
    uid INT NOT NULL,
    pid INT NOT NULL,
    tlabal VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    insert_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE igg_user_activity_log(
    uid INT NOT NULL,
    pid INT NOT NULL,
    tlabal VARCHAR(20) NOT NULL,
    act VARCHAR(20) NOT NULL,
    insert_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()
);
