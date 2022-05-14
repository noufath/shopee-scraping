-- public.customer definition

-- Drop table;

-- DROP TABLE public.customer;

CREATE TABLE public.customer (
	shopid varchar NOT NULL,
	userid varchar NULL,
	account jsonb NULL,
	follower_count int4 NULL DEFAULT 0,
	is_official_shop bool NULL DEFAULT false,
	is_preferred_plus_seller bool NULL DEFAULT false,
	is_shopee_verified bool NULL DEFAULT false,
	item_count int4 NULL DEFAULT 0,
	"name" varchar NULL,
	place varchar NULL,
	rating_bad int4 NULL DEFAULT 0,
	rating_good int4 NULL DEFAULT 0,
	rating_normal int4 NULL DEFAULT 0,
	rating_star int4 NULL DEFAULT 0,
	response_rate int4 NULL DEFAULT 0,
	response_time int4 NULL DEFAULT 0,
	shop_location varchar NULL,
	show_official_shop_label bool NULL DEFAULT false,
	vacation bool NULL DEFAULT false,
	last_active_time int8 NULL,
	session_info jsonb NULL,
	ctime int8 NULL,
	CONSTRAINT customer_pkey PRIMARY KEY (shopid)
);

-- public.item definition

-- Drop table

-- DROP TABLE public.item;

CREATE TABLE public.item (
	itemid varchar NOT NULL,
	shopid varchar NOT NULL,
	"name" varchar NOT NULL,
	label_ids json NULL,
	image varchar NULL,
	images varchar NULL,
	currency varchar(5) NULL,
	stock int8 NULL DEFAULT 0,
	status int4 NULL,
	sold int4 NULL DEFAULT 0,
	historical_sold int8 NULL DEFAULT 0,
	liked bool NULL DEFAULT false,
	liked_count int8 NULL DEFAULT 0,
	view_count varchar NULL DEFAULT 0,
	catid varchar NULL,
	brand varchar NOT NULL,
	cmt_count int4 NULL DEFAULT 0,
	flag int4 NULL DEFAULT 0,
	cb_option int4 NULL DEFAULT 0,
	item_status varchar NULL,
	price float8 NULL DEFAULT 0,
	price_min float8 NULL DEFAULT 0,
	price_max float8 NULL DEFAULT 0,
	price_min_before_discount float8 NULL DEFAULT 0,
	price_max_before_discount float8 NULL DEFAULT 0,
	hidden_price_display varchar NULL DEFAULT 0,
	price_before_discount float8 NULL DEFAULT 0,
	has_lowest_price_guarantee bool NULL DEFAULT false,
	show_discount float4 NULL DEFAULT 0,
	raw_discount float4 NULL DEFAULT 0,
	discount varchar NULL,
	is_category_failed bool NULL DEFAULT false,
	size_chart varchar NULL,
	video_info_list varchar NULL,
	tier_variations jsonb NULL,
	item_rating jsonb NULL,
	item_type int2 NULL DEFAULT 0,
	reference_item_id varchar NULL,
	transparent_background_image varchar NULL,
	is_adult bool NULL DEFAULT false,
	badge_icon_type int2 NULL DEFAULT 0,
	shopee_verified bool NULL DEFAULT false,
	is_official_shop bool NULL DEFAULT false,
	show_official_shop_label bool NULL DEFAULT false,
	show_shopee_verified_label bool NULL DEFAULT false,
	show_official_shop_label_in_title bool NULL DEFAULT false,
	is_cc_installment_payment_eligible bool NULL DEFAULT false,
	is_non_cc_installment_payment_eligible bool NULL DEFAULT false,
	coin_earn_label varchar NULL,
	show_free_shipping varchar NULL,
	preview_info varchar NULL,
	coin_info varchar NULL,
	exclusive_price_info varchar NULL,
	bundle_deal_id int8 NULL DEFAULT 0,
	bundle_deal_info varchar NULL,
	is_group_buy_item varchar NULL,
	has_group_buy_stock varchar NULL,
	group_buy_info varchar NULL,
	welcome_package_type int2 NULL DEFAULT 0,
	welcome_package_info varchar NULL,
	add_on_deal_info varchar NULL,
	can_use_wholesale bool NULL DEFAULT false,
	can_use_bundle_deal bool NULL DEFAULT false,
	is_preferred_plus_seller bool NULL DEFAULT false,
	shop_location varchar NULL,
	has_model_with_available_shopee_stock bool NULL DEFAULT false,
	voucher_info varchar NULL,
	can_use_cod bool NULL DEFAULT false,
	is_on_flash_sale bool NULL DEFAULT false,
	spl_installment_tenure varchar NULL,
	is_live_streaming_price varchar NULL,
	is_mart bool NULL DEFAULT false,
	pack_size varchar NULL,
	ctime int8 NULL
);
CREATE UNIQUE INDEX item_itemid_idx ON public.item USING btree (itemid);

-- public.main_category definition

-- Drop table

-- DROP TABLE public.main_category;

CREATE TABLE public.main_category (
	catid varchar(50) NOT NULL,
	display_name varchar(255) NULL,
	"name" varchar(255) NULL,
	parent_category varchar(50) NULL,
	is_adult text NULL,
	block_buyer_platform text NULL,
	sort_weight int4 NULL,
	CONSTRAINT maincategory PRIMARY KEY (catid)
);

-- public.sub_category definition

-- Drop table

-- DROP TABLE public.sub_category;

CREATE TABLE public.sub_category (
	catid varchar(50) NOT NULL,
	display_name varchar(255) NULL,
	"name" varchar(255) NULL,
	parent_category varchar(50) NULL,
	is_adult text NULL,
	block_buyer_platform text NULL,
	sort_weight int4 NULL,
	sub_sub jsonb NULL,
	CONSTRAINT sub_category_pkey PRIMARY KEY (catid)
);


-- public.sub_category definition

-- Drop table

-- DROP TABLE public.sub_category;

CREATE TABLE public.sub_category (
	catid varchar(50) NOT NULL,
	display_name varchar(255) NULL,
	"name" varchar(255) NULL,
	parent_category varchar(50) NULL,
	is_adult text NULL,
	block_buyer_platform text NULL,
	sort_weight int4 NULL,
	sub_sub jsonb NULL,
	CONSTRAINT sub_category_pkey PRIMARY KEY (catid)
);


public.sub_category foreign keys

ALTER TABLE public.sub_category ADD CONSTRAINT fk_maincategory FOREIGN KEY (parent_category) REFERENCES public.main_category(catid) ON DELETE CASCADE;

